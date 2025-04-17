from pydantic import BaseModel, validator, ValidationError
from typing import Optional, List

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

class FilmPiattaformaSchema(BaseModel):
    id: int
    film_id: int
    piattaforma_id: int

    class Config:
        from_attributes = True

# Risultati specifici per query
class FilmResult(BaseModel):
    id: int
    name: str
    anno: Optional[int]

class RegistaResult(BaseModel):
    id: int
    name: str
    anno: Optional[int]

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

class FilmInput(BaseModel):
    Titolo: str
    Regista: str
    Età_Autore: int
    Anno: int 
    Genere: str
    Piattaforme: List[str]

    @validator("Piattaforme")
    def massimo_due(cls, v):
        if len(v) > 2:
            raise ValueError("Massimo due piattaforme per film")
        return v
    
    class Config:
        from_attributes = True

class TSVInput(BaseModel):
    contenuto: str

class CSVInput(BaseModel):
    contenuto: str