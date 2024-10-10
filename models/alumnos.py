from config.database import Base
from sqlalchemy import Column, Integer, String

class Alumno(Base):
    __tablename__ = "alumnos"
    id = Column(Integer, primary_key = True)
    nombre = Column(String)
    edad = Column(Integer)
