from sqlalchemy import Column, Integer, String, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Regista(Base):
    __tablename__ = 'Regista'

    id = Column(Integer, primary_key=True)
    nome = Column(String, unique=True, nullable=False)
    eta = Column(Integer)

    film = relationship("Film", back_populates="regista")

class Genere(Base):
    __tablename__ = 'Genere'

    id = Column(Integer, primary_key=True)
    nome = Column(String(50))

    film = relationship("Film", back_populates="genere")

class Piattaforma(Base):
    __tablename__ = 'Piattaforma'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), unique=True, nullable=False)

    film_assoc = relationship("FilmPiattaforma", back_populates="piattaforma")   

class Film(Base):
    __tablename__ = 'Film'

    id = Column(Integer, primary_key=True)
    titolo = Column(String, nullable=False)
    anno = Column(Integer, nullable=False)
    regista_id = Column(Integer, ForeignKey('Regista.id'))
    genere_id = Column(Integer, ForeignKey('Genere.id'))    

    regista = relationship("Regista", back_populates="film")
    genere = relationship("Genere", back_populates="film")
    piattaforme = relationship("FilmPiattaforma", back_populates="film")

    __table_args__ = (UniqueConstraint('titolo', 'anno'),)
class FilmPiattaforma(Base):
    __tablename__ = 'Film_Piattaforma'

    id = Column(Integer, primary_key=True)
    film_id = Column(Integer, ForeignKey('Film.id'))
    piattaforma_id = Column(Integer, ForeignKey('Piattaforma.id'))

    film = relationship("Film", back_populates="piattaforme")
    piattaforma = relationship("Piattaforma", back_populates="film_assoc")