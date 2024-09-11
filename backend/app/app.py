from fastapi import FastAPI

app = FastAPI()

@app.get("/diagram")
def get_diagram():
    return {"www.foto.com"}