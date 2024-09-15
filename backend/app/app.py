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

#Se reciben los parámetros mediante una solicitud HTTP con los argumentos, y luego se arma el diccionario data

@app.get("/diagram")
def get_diagram(
    bd: str = Query(...),
    host: str = Query(...),
    port: int = Query(...),
    user: str = Query(...),
    password: str = Query(...),
    database: str = Query(...)
):
    """data = {
        "bd": bd,
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "database": database
    }"""
    
    # Parametros para solicitud en MySQL
    """
    dataBase = "proyecto"
    hosteador = "localhost"
    puerto = 3306
    usuario = "root"
    contrasena = ""
    baseDatos = "proyecto"
    """

    # Parametros para solicitud en PostgreSQL
    """"dataBase = "proyecto"
    hosteador = "COMPUTER"
    puerto = 4096
    usuario = "postgres"
    contrasena = "Windows Authentication"
    baseDatos = "proyecto" """

    # Parametros para solicitud en SQL Server
    """driver = "SQL Server"
    server = "localhost"
    database = "proyecto"
    uid = "sa"  # Tu nombre de usuario
    pwd = "123"  # Tu contraseña"""

    # Data enviada a la función conexión para SQL SERVER
    """dataSqlServer = {
        "driver": driver,
        "server": server,
        "database": database,
        "uid": uid,
        "pwd": pwd
    }"""

    # Data enviada a la función conexión para MySQL y PostgreSQL
    """data = {
        "bd": dataBase,
        "host": hosteador,
        "port": puerto,
        "user": usuario,
        "password": contrasena,
        "database": baseDatos
    }"""
    #El information schema de cualquier de las 3 BD
    schema = None

    #Formatear el esquema en PlantUML

    #Consulta MySQL
    """schema = connect_mysql(data)
    formatted_schema = format_schema(schema)
    encode_text = encode_plantuml(formatted_schema)
    generate_uml_image(encode_text)
    # Obtener el enlace de la imagen generada por PlantUML
    uml_url = generate_plantuml_image(formatted_schema)"""
    
    #Consulta PostgreSQL
    """schema = connect_postgres(data)
    formatted_schema = format_schema(schema)
    encode_text = encode_plantuml(formatted_schema)
    generate_uml_image(encode_text)
    uml_url = generate_plantuml_image(formatted_schema)"""


    data = {
        "bd": bd,
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "database": database
    }

    #Consulta SQL Server
    schema = connect_sqlserver(data)
    formatted_schema = format_schema(schema)
    encode_text = encode_plantuml(formatted_schema)
    generate_uml_image(encode_text)
    uml_url = generate_plantuml_image(formatted_schema)

    uml_url = None
    return {"url": uml_url}


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
        encode_text = encode_plantuml(formatted_schema)
        generate_uml_image(encode_text)
        
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


"""Formatea el scheme recibido de la conexión a las BD para usarse en plantUML"""
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

"""Se hace una solicitud HTTP a plantUML y se recibe """
def generate_plantuml_image(uml_code):
    try:
        # Endpoint de PlantUML para la generación de diagramas
        plantuml_url = "http://www.plantuml.com/plantuml/svg/~1"

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


def encode_plantuml(text):
    # Remove the zlib header (first two bytes) and the checksum (last four bytes)
    zlibbed_str = zlib.compress(text.encode('utf-8'))
    compressed_string = zlibbed_str[2:-4]
    
    # Encode to base64
    encoded = base64.b64encode(compressed_string)
    
    # Translate base64 to PlantUML's encoding alphabet
    plantuml_alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'
    base64_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    translation_table = str.maketrans(base64_alphabet, plantuml_alphabet)
    
    # Return the translated string
    return encoded.decode('utf-8').translate(translation_table)


def generate_uml_image(encoded_text):
    # Base URL for PlantUML server
    base_url = "http://www.plantuml.com/plantuml/png/"
    
    # Full URL with encoded UML text
    full_url = base_url + encoded_text
    
    # Make the request
    response = requests.get(full_url)
    
    # Save the resulting image
    if response.status_code == 200:
        with open("uml_diagram.png", "wb") as file:
            file.write(response.content)
        print("Image generated and saved as uml_diagram.png")
    else:
        print(f"Error generating diagram: {response.status_code}")
