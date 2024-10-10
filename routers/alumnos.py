from fastapi.encoders import jsonable_encoder
from config.database import Session
from services.alumnos import AlumnoService



from typing import Optional
from fastapi.params import Query
from fastapi.responses import HTMLResponse, JSONResponse

from schemas.alumnos import Alumno

from fastapi import APIRouter, HTTPException, Path
alumno_router=APIRouter()



alumnos = [
    {"id": 1, "nombre": "Juan Pérez", "edad": 20},
    {"id": 2, "nombre": "María García", "edad": 22},
    {"id": 3, "nombre": "Luis Rodríguez", "edad": 21}
]




@alumno_router.get("/alumnos", tags=["Alumnos - Arreglos"])
def getAlumnos():
    return alumnos


@alumno_router.get("/alumnos/tablaAlumnos", tags=["Alumnos - formato Tabla"])
async def get_alumnos():
    table_html = "<table border='1'>\n<tr><th>ID</th><th>Nombre</th><th>Edad</th></tr>"
    for alumno in alumnos:
        table_html += f"\n<tr><td>{alumno['id']}</td><td>{alumno['nombre']}</td><td>{alumno['edad']}</td></tr>"
    table_html += "\n</table>"
    return HTMLResponse(content=table_html)


@alumno_router.get("/alumnos/Pr1/{id}", tags=["Alumnos - Parametros de ruta"])
def get_alumno(id: int):
    return id


@alumno_router.get("/alumnos/Pr2/{id}", tags=["Alumnos - Parametros de ruta 2"])
def get_alumno(id: int):
    for alumno in alumnos:
        if alumno["id"] == id:
            return alumno
    return []




@alumno_router.get("/alumnos/id/{id}", tags=["Alumnos - Parametros de ruta 3"])
def get_alumno(id: int):
    # Buscamos al alumno por su ID
    #alumno = next((alumno for alumno in alumnos if alumno["id"] == id), None)

    alumno = None
    for a in alumnos:
        if a["id"] == id:
            alumno = a
            break
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




@alumno_router.post("/alumnos/esquemas/", tags=["Alumnos - Esquemas"])
async def crear_alumno(alumno: Alumno):
    return {"mensaje": "Alumno creado", "alumno": alumno}



@alumno_router.post('/alumnos/crear', tags=['Alumnos - Crear'])
def createAlumno(Alumno: Alumno):
    alumnos.append(Alumno)
    return alumnos



@alumno_router.delete("/alumnos/borrar/{id}", tags=["Alumno - Borrar"])
async def BorrarAlumno(id: int):
    for alumno in alumnos:
        if alumno["id"] == id:
            alumnos.remove(alumno)
    return alumnos


@alumno_router.put("/alumnos/modificar/{id}", tags=["Alumno - Modificar"])
async def ModificarAlumno(id:int,Alumno:Alumno ):
    for alumno in alumnos:
        if alumno["id"] == id:
            alumno["nombre"] = Alumno.nombre
            alumno["edad"] = Alumno.edad
            return {"mensaje": "Alumno modificado correctamente", "alumno": alumno}
    return {"mensaje": "No se encontro el alumno que se queria modificar"}




@alumno_router.get("/alumnos/validacion", tags=["Alumnos - Validacion Query"])
def get_alumnos(
    edad_min: Optional[int] = Query(None, ge=18, le=30),
    edad_max: Optional[int] = Query(None, ge=18, le=30)
):
    resultados = alumnos
    
    if edad_min is not None:
        resultados = [alumno for alumno in resultados if alumno["edad"] >= edad_min]
    
    if edad_max is not None:
        resultados = [alumno for alumno in resultados if alumno["edad"] <= edad_max]
    
    return JSONResponse(content=resultados)




@alumno_router.get("/alumnos/SC/{id}", tags=["Alumnos - Codigos de estado"])
async def get_alumno(id: int = Path(ge=1, le=2000)):
    for alumno in alumnos:
        if alumno["id"] == id:
            return JSONResponse(content=alumno, status_code=200)
    
    return JSONResponse(content={"detail": "Alumno no encontrado"}, status_code=404)



@alumno_router.get("/alumnos/E/{id}", tags=["Alumnos - Excepciones"])
async def get_alumno(id: int = Path(ge=1, le=2000)):
    for alumno in alumnos:
        if alumno["id"] == id:
            return JSONResponse(content=alumno, status_code=200)
    raise HTTPException(status_code=404, detail="Alumno no encontrado")


@alumno_router.post('/alumnos/crearAlumnoS', tags=['alumnos - Crear con Servicios'], response_model=dict, status_code=201)
def create_Alumno(alumno: Alumno):
    db = Session()
    AlumnoService(db).create_alumno(alumno)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado correctamente el alumno."})



@alumno_router.get('/alumnos/getUsers/', tags=['Alumnos - Select ALL con Servicios '], status_code=200)
def get_alumnos():
    db = Session()
    result = AlumnoService(db).get_alumnos()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))  


@alumno_router.get('/alumnos/getUsers/{id}', tags=['Alumnos - Select ONE con Servicios'], response_model=Alumno)
def get_Alumno(id: int ) -> Alumno:
    db = Session()
    result=AlumnoService(db).get_alumno(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "Alumno No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))  


@alumno_router.put('/alumnos/update/{id}', tags=['Alumnos - Update con Servicios'], status_code=200)
def update_Alumno(id: int, Alumno: Alumno):
    db = Session()
    result=AlumnoService(db).get_alumno(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "Alumno No encontrado"})
    else:
        AlumnoService(db).update_alumno(id,Alumno)
        return JSONResponse(status_code=200, content={"message": "Se han modificado los datos del alumno"})


@alumno_router.delete('/alumnos/delete/{id}', tags=['Alumnos _ delete con services'], status_code=200)
def update_Alumno(id: int):
    db = Session()
    result=AlumnoService(db).get_alumno(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "Alumno No encontrado"})
    else:
        AlumnoService(db).delete_alumno(id)
        return JSONResponse(status_code=200, content={"message": "Se han eliminado el registro"})
