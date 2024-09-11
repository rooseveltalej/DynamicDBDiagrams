from fastapi import FastAPI

app = FastAPI()

def connect_postgres():

    return

def connect_mysql():

    return

def connect_sqlserver():
    
    return


@app.get("/diagram")
def get_diagram(data):
    if data["bd"] == "postgres":
        connect_postgres()
    elif data["bd"] == "mysql":
        connect_mysql()
    else:
        connect_sqlserver()

    return {"url": "www.foto.com"}
