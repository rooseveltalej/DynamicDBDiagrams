from fastapi import FastAPI, HTTPException, Query
from db_connections import connect_mysql, connect_postgres, connect_sqlserver
from plantuml_request import format_schema, encode_plantuml, generate_uml_image

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
    
    #El information schema de cualquier de las 3 BD
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
        
        encode_text = encode_plantuml(formatted_schema)
        
        # Obtener el enlace de la imagen generada por PlantUML
        uml_url = generate_uml_image(encode_text)
        
        return {"url": uml_url}

    except HTTPException as e:
        raise e  # Re-lanza excepciones HTTP preexistentes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")



