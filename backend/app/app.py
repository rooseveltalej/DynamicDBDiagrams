import base64
import zlib
from fastapi import FastAPI, HTTPException, Query
import psycopg2
import mysql.connector
import pyodbc
import requests

app = FastAPI()

@app.get("/")
def is_running():
    return {"status": "running"}

@app.get("/diagram")
def get_diagram(
    bd: str = Query(...),
    host: str = Query(...),
    port: int = Query(...),
    user: str = Query(...),
    password: str = Query(...),
    database: str = Query(...)
):
    data = {
        "bd": bd,
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "database": database
    }
    
    schema = None

    try:
        # Conectar a la base de datos según el tipo
        if bd == "postgres":
            schema = connect_postgres(data)
        elif bd == "mysql":
            schema = connect_mysql(data)
        elif bd == "sqlserver":
            schema = connect_sqlserver(data)
        else:
            raise HTTPException(status_code=400, detail="Tipo de base de datos no soportado.")
        
        # Formatear el esquema en PlantUML
        formatted_schema = format_schema(schema)
        
        # Obtener el enlace de la imagen generada por PlantUML
        uml_url = generate_plantuml_image(formatted_schema)
        
        return {"url": uml_url}

    except HTTPException as e:
        raise e  # Re-lanza excepciones HTTP preexistentes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")


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
                    AND c.column_name = (
                        SELECT
                            kcu.column_name
                        FROM
                            information_schema.key_column_usage kcu
                        WHERE
                            kcu.constraint_name = tc.constraint_name
                            AND kcu.table_schema = tc.table_schema
                            AND kcu.table_name = tc.table_name
                    )
                WHERE
                    c.table_schema = %s
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
                    AND tc.table_schema = %s
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
            WITH table_info AS (
                SELECT
                    table_schema,
                    table_name,
                    column_name,
                    data_type,
                    CASE
                        WHEN column_key = 'PRI' THEN 'PK'
                        ELSE ''
                    END AS constraint_type
                FROM
                    information_schema.columns
                WHERE
                    table_schema = %s
            ),
            foreign_keys AS (
                SELECT
                    k.table_schema AS source_schema,
                    k.table_name AS source_table,
                    k.column_name AS source_column,
                    c.table_name AS target_table,
                    c.column_name AS target_column
                FROM
                    information_schema.key_column_usage k
                JOIN
                    information_schema.constraint_column_usage c
                    ON k.constraint_name = c.constraint_name
                WHERE
                    k.referenced_table_name IS NOT NULL
                    AND k.table_schema = %s
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
        raise HTTPException(status_code=500, detail=f"Error en MySQL: {str(e)}")


def connect_sqlserver(data):
    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={data['host']},{data['port']};DATABASE={data['database']};UID={data['user']};PWD={data['password']}"
        )
        cur = conn.cursor()
        cur.execute("""
            WITH table_info AS (
                SELECT
                    t.TABLE_SCHEMA,
                    t.TABLE_NAME,
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
                    AND pk.CONSTRAINT_NAME LIKE 'PK%'
                WHERE
                    t.TABLE_TYPE = 'BASE TABLE'
                    AND c.TABLE_SCHEMA = 'dbo'
            ),
            foreign_keys AS (
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
        """)
        schema = cur.fetchall()
        cur.close()
        conn.close()
        return schema
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en SQL Server: {str(e)}")


def format_schema(schema):
    tables = {}
    relationships = set()

    for row in schema:
        table_name = row[1]  # Cambiado a índice 1 para el nombre de la tabla
        column_name = row[2]
        data_type = row[3]
        pk_status = row[4]
        fk_source_table = row[5]
        fk_source_column = row[6]
        fk_target_table = row[7]
        fk_target_column = row[8]

        if table_name not in tables:
            tables[table_name] = []

        tables[table_name].append((column_name, data_type, pk_status))

        if fk_source_table and fk_target_table:
            relationships.add((fk_source_table, fk_source_column, fk_target_table, fk_target_column))

    uml_output = "@startuml\n\n"

    for table, columns in tables.items():
        uml_output += f"entity {table} {{\n"
        for column, data_type, pk_status in columns:
            uml_output += f"  + {column}: {data_type}\n" if pk_status == 'PK' else f"  {column}: {data_type}\n"
        uml_output += "}\n\n"

    for source_table, source_column, target_table, target_column in relationships:
        uml_output += f"{source_table} ||--o{{ {target_table} : \"{source_column} -> {target_column}\"\n"

    uml_output += "@enduml"

    return uml_output


def generate_plantuml_image(uml_code):
    try:
        # Endpoint de PlantUML para la generación de diagramas
        plantuml_url = "http://www.plantuml.com/plantuml/png/~1"

        # Codificar el código UML a formato DEFLATE
        compressed_data = zlib.compress(uml_code.encode(), level=zlib.Z_BEST_COMPRESSION)
        encoded_data = base64.urlsafe_b64encode(compressed_data).decode()

        # Realizar la solicitud HTTP a PlantUML
        response = requests.get(f"{plantuml_url}{encoded_data}")

        if response.status_code == 200:
            return response.url
        else:
            raise Exception(f"Error al generar la imagen: {response.status_code}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar imagen de PlantUML: {str(e)}")
