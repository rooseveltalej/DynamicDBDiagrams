from fastapi import HTTPException
import psycopg2
import mysql.connector
import pyodbc

def connect_postgres(data):
    try:
        conn = psycopg2.connect(
            dbname=data["database"],
            user=data["user"],
            password=data["password"],
            host=data["host"],
            port=data["port"]
        )
        cur = conn.cursor()
        cur.execute("""
            WITH table_info AS (
                SELECT
                    c.table_schema,
                    c.table_name,
                    c.column_name,
                    c.data_type,
                    CASE
                        WHEN tc.constraint_type = 'PRIMARY KEY' THEN 'PK'
                        ELSE ''
                    END AS constraint_type
                FROM
                    information_schema.columns c
                LEFT JOIN
                    information_schema.table_constraints tc
                    ON c.table_schema = tc.table_schema
                    AND c.table_name = tc.table_name
                LEFT JOIN
                    information_schema.key_column_usage kcu
                    ON kcu.table_schema = tc.table_schema
                    AND kcu.table_name = tc.table_name
                    AND kcu.column_name = c.column_name
                    AND kcu.constraint_name = tc.constraint_name
                WHERE
                    c.table_schema = 'public'
                    AND tc.constraint_type = 'PRIMARY KEY'
            ),
            foreign_keys AS (
                SELECT
                    tc.table_schema AS source_schema,
                    tc.table_name AS source_table,
                    kcu.column_name AS source_column,
                    ccu.table_name AS target_table,
                    ccu.column_name AS target_column
                FROM
                    information_schema.table_constraints tc
                JOIN
                    information_schema.key_column_usage kcu
                    ON tc.constraint_name = kcu.constraint_name
                JOIN
                    information_schema.constraint_column_usage ccu
                    ON tc.constraint_name = ccu.constraint_name
                WHERE
                    tc.constraint_type = 'FOREIGN KEY'
                    AND tc.table_schema = 'public'
            )
            SELECT
                ti.table_schema,
                ti.table_name,
                ti.column_name,
                ti.data_type,
                ti.constraint_type AS pk_status,
                fk.source_table AS fk_source_table,
                fk.source_column AS fk_source_column,
                fk.target_table AS fk_target_table,
                fk.target_column AS fk_target_column
            FROM
                table_info ti
            LEFT JOIN
                foreign_keys fk
                ON ti.table_name = fk.source_table
                AND ti.column_name = fk.source_column
            ORDER BY
                ti.table_schema,
                ti.table_name,
                ti.column_name;

        """, (data["database"], data["database"]))
        schema = cur.fetchall()
        cur.close()
        conn.close()
        return schema
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en PostgreSQL: {str(e)}")

def connect_mysql(data):
    try:
        conn = mysql.connector.connect(
            user=data["user"],
            password=data["password"],
            host=data["host"],
            database=data["database"],
            port=data["port"]
        )
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                NULL AS 'Tabla', -- Placeholder para cumplir con el índice de la función
                c.table_name AS 'Tabla',
                c.column_name AS 'Columna',
                c.data_type AS 'Tipo de Dato',
                CASE 
                    WHEN kcu.constraint_name IS NOT NULL AND tc.constraint_type = 'PRIMARY KEY' THEN 'PK'
                    ELSE NULL
                END AS 'Es PK',
                CASE 
                    WHEN tc.constraint_type = 'FOREIGN KEY' THEN c.table_name
                    ELSE NULL
                END AS 'Tabla Origen FK',
                CASE 
                    WHEN tc.constraint_type = 'FOREIGN KEY' THEN c.column_name
                    ELSE NULL
                END AS 'Columna Origen FK',
                kcu.referenced_table_name AS 'Tabla Objetivo FK',
                kcu.referenced_column_name AS 'Columna Objetivo FK'
            FROM 
                information_schema.columns c
                LEFT JOIN information_schema.key_column_usage kcu 
                    ON c.table_name = kcu.table_name 
                    AND c.column_name = kcu.column_name 
                    AND c.table_schema = kcu.table_schema
                LEFT JOIN information_schema.table_constraints tc
                    ON tc.constraint_name = kcu.constraint_name
                    AND tc.table_schema = c.table_schema
                    AND tc.table_name = c.table_name
            WHERE 
                c.table_schema = %s
            ORDER BY 
                c.table_name, c.ordinal_position;
        """, (data["database"],))  # Pasar el parámetro como una tupla
        schema = cur.fetchall()
        cur.close()
        conn.close()
        return schema
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en MySQL: {str(e)}")

def connect_sqlserver(data):
    try:
        # Construct the connection string
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={data['host']},{data['port']};"
            f"DATABASE={data['database']};"
            f"UID={data['user']};"
            f"PWD={data['password']}"
        )

        # Connect to the database
        conn = pyodbc.connect(conn_str)
        cur = conn.cursor()

        # Execute the query
        cur.execute("""
            WITH TableInfo AS (
                SELECT
                    c.TABLE_SCHEMA,
                    c.TABLE_NAME,
                    c.COLUMN_NAME,
                    c.DATA_TYPE,
                    CASE 
                        WHEN pk.COLUMN_NAME IS NOT NULL THEN 'PK'
                        ELSE ''
                    END AS constraint_type
                FROM
                    INFORMATION_SCHEMA.COLUMNS c
                JOIN
                    INFORMATION_SCHEMA.TABLES t
                    ON c.TABLE_NAME = t.TABLE_NAME
                    AND c.TABLE_SCHEMA = t.TABLE_SCHEMA
                LEFT JOIN
                    INFORMATION_SCHEMA.KEY_COLUMN_USAGE pk
                    ON c.TABLE_NAME = pk.TABLE_NAME
                    AND c.COLUMN_NAME = pk.COLUMN_NAME
                    AND pk.CONSTRAINT_NAME IN (
                        SELECT CONSTRAINT_NAME 
                        FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS 
                        WHERE CONSTRAINT_TYPE = 'PRIMARY KEY'
                    )
                WHERE
                    t.TABLE_TYPE = 'BASE TABLE'
            ),
            ForeignKeys AS (
                SELECT
                    fk.TABLE_SCHEMA AS source_schema,
                    fk.TABLE_NAME AS source_table,
                    fk.COLUMN_NAME AS source_column,
                    ccu.TABLE_NAME AS target_table,
                    ccu.COLUMN_NAME AS target_column
                FROM
                    INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS rc
                JOIN
                    INFORMATION_SCHEMA.KEY_COLUMN_USAGE fk
                    ON rc.CONSTRAINT_NAME = fk.CONSTRAINT_NAME
                JOIN
                    INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE ccu
                    ON rc.UNIQUE_CONSTRAINT_NAME = ccu.CONSTRAINT_NAME
            )
            SELECT
                ti.TABLE_SCHEMA AS 'Esquema',
                ti.TABLE_NAME AS 'Tabla',
                ti.COLUMN_NAME AS 'Columna',
                ti.DATA_TYPE AS 'Tipo de Dato',
                CASE
                    WHEN ti.constraint_type = 'PK' THEN 'PK'
                    ELSE NULL
                END AS 'Es PK',
                CASE
                    WHEN fk.source_table IS NOT NULL THEN fk.source_table
                    ELSE NULL
                END AS 'Tabla Origen FK',
                CASE
                    WHEN fk.source_column IS NOT NULL THEN fk.source_column
                    ELSE NULL
                END AS 'Columna Origen FK',
                fk.target_table AS 'Tabla Objetivo FK',
                fk.target_column AS 'Columna Objetivo FK'
            FROM
                TableInfo ti
            LEFT JOIN
                ForeignKeys fk
                ON ti.TABLE_NAME = fk.source_table
                AND ti.COLUMN_NAME = fk.source_column
            ORDER BY
                ti.TABLE_SCHEMA,
                ti.TABLE_NAME,
                ti.COLUMN_NAME;
        """)

        # Fetch the results
        schema = cur.fetchall()

        # Close the cursor and connection
        cur.close()
        conn.close()

        return schema

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en SQL Server: {str(e)}")
