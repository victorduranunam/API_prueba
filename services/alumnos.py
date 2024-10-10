from sqlalchemy.orm import Session
from models.alumnos import Alumno as AlumnoModel
from schemas.alumnos import Alumno 

class AlumnoService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_alumno(self, alumno: Alumno):
        newAlumno=AlumnoModel(**alumno.model_dump())
        self.db.add(newAlumno)
        self.db.commit()
        return
    
    def get_alumnos(self):
        result = self.db.query(AlumnoModel).all()
        return result


    def get_alumno(self,id:int):
        result = self.db.query(AlumnoModel).filter(AlumnoModel.id == id).first()
        return result

    def update_alumno(self,id:int, data: Alumno):
        alumno = self.db.query(AlumnoModel).filter(AlumnoModel.id == id).first()
        alumno.nombre=data.nombre
        alumno.edad=data.edad
        self.db.commit()
        return

    def delete_alumno(self,id:int):
        result = self.db.query(AlumnoModel).filter(AlumnoModel.id == id).first()
        self.db.delete(result)
        self.db.commit()
        return
