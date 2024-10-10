from fastapi import FastAPI
from typing import Optional
from fastapi.responses import HTMLResponse


app=FastAPI()
app.title="MyAPI"
app.version="1.0"
app.description="Api de prueba"



alumnos = [
    {"id": 1, "nombre": "Juan Pérez", "edad": 20},
    {"id": 2, "nombre": "María García", "edad": 22},
    {"id": 3, "nombre": "Luis Rodríguez", "edad": 21}
]



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


@app.get("/alumnos", tags=["Alumnos - Arreglos"])
def getAlumnos():
    return alumnos


@app.get("alumnos/tablaAlumnos", tags=["Alumnos - formato Tabla"])
async def get_alumnos():
    table_html = "<table border='1'>\n<tr><th>ID</th><th>Nombre</th><th>Edad</th></tr>"
    for alumno in alumnos:
        table_html += f"\n<tr><td>{alumno['id']}</td><td>{alumno['nombre']}</td><td>{alumno['edad']}</td></tr>"
    table_html += "\n</table>"
    return HTMLResponse(content=table_html)


@app.get("/alumnos/{id}", tags=["Alumnos - Parametros de ruta"])
def get_alumno(id: int):
    return id


@app.get("/alumnos/PR/{id}", tags=["Alumnos - Parametros de ruta 2"])
def get_alumno(id: int):
    for alumno in alumnos:
        if alumno["id"] == id:
            return alumno
    return []

@app.get("/alumnos/PR2/{id}", tags=["Alumnos - Parametros de ruta 3"])
def get_alumno(id: int):
    # Buscamos al alumno por su ID
    alumno = next((alumno for alumno in alumnos if alumno["id"] == id), None)
    if alumno is None:
        datosAlumno = f"""
        <html>
        <head>
            <title>Alumno no encontrado</title>
        </head>
        <body>
            <h2>Alumno no encontrado</h2>
            <p>El alumno con id={id} no se ha encontrado en nuestra base de datos.</p>
        </body>
        </html>
        """
    else:
        # Devolvemos los datos del alumno en formato HTML
        datosAlumno = f"""
        <html>
        <head>
            <title>Datos del Alumno</title>
        </head>
        <body>
            <h2>Datos del alumno con id={id}</h2>
            <p><strong>Nombre:</strong> {alumno['nombre']}</p>
            <p><strong>Edad:</strong> {alumno['edad']}</p>
        </body>
        </html>
        """
    return HTMLResponse(content=datosAlumno)
