from typing import Optional
from pydantic import BaseModel, Field

class Alumno(BaseModel):
    id: Optional[int]=None
    nombre: str
    edad: int
