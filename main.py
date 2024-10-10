from fastapi import FastAPI
from typing import Optional
from fastapi.responses import HTMLResponse
from routers.alumnos import alumno_router



app=FastAPI()
app.title="MyAPI"
app.version="1.0"
app.description="Api de prueba"




@app.get('/', tags=["Home"])
def message(name: Optional[str] = None):
    return "Hola Mundo"



@app.get('/var', tags=["Manejando Variables"])
def message(name: Optional[str] = None):
    if name:
        return f"Hola {name}"
    else: 
        return "Hola Mundo"



@app.get('/varhtml', tags=["Agregando formato HTML"])
def message(name: Optional[str] = None):
    if name:
        return HTMLResponse(f"<h1> Hola, {name} </h1>")
    else: 
        return "Hola Mundo"


app.include_router(alumno_router)