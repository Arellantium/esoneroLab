from pydantic import BaseModel
from typing import Optional

# Schemi base, compatibili con SQLAlchemy
class FilmSchema(BaseModel):
    id: int
    titolo: str
    anno: int

    class Config:
        from_attributes = True

class RegistaSchema(BaseModel):
    id: int
    nome: str
    eta: int

    class Config:
        from_attributes = True

class GenereSchema(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True

class PiattaformaSchema(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True

# Risultati specifici per query
class FilmResult(BaseModel):
    titolo: str
    anno: int

    class Config:
        from_attributes = True

class RegistaResult(BaseModel):
    nome: str

    class Config:
        from_attributes = True

class FilmConRegistaEtaResult(BaseModel):
    titolo: str
    regista: str
    eta: int

    class Config:
        from_attributes = True

class RegistaMultiFilmResult(BaseModel):
    nome: str
    numero_film: int

    class Config:
        from_attributes = True

class SchemaColumn(BaseModel):
    table_name: str
    column_name: str
