from typing import Tuple, Type
from schemas import FilmResult, RegistaResult, FilmConRegistaEtaResult, RegistaMultiFilmResult, SchemaColumn, FilmInput, CSVInput
from models import Regista, Genere, Piattaforma, Film, FilmPiattaforma
import re
import pandas as pd
from pydantic import ValidationError
from fastapi import HTTPException
import csv
from io import StringIO

ANNO_REGEX = r"^elenca i film del (\d{4})\.$"
ANNI_REGEX = r"^quali film sono stati fatti da un regista di almeno (\d+) anni\?$"

def match_question_to_sql(question: str) -> Tuple[str, Type, str]:
    question = question.lower().strip()
    print(question)

    if re.match(ANNO_REGEX, question):
        anno = question.replace("elenca i film del ", "").replace(".", "").strip()
        sql = f"""
        SELECT id, titolo AS name, anno 
        FROM Film 
        WHERE anno = {anno}
        """
        return sql, FilmResult, "film"

    elif question == "quali sono i registi presenti su netflix?":
        sql = """
        SELECT DISTINCT Regista.id, Regista.nome AS name, NULL AS anno
        FROM Regista
        JOIN Film ON Film.regista_id = Regista.id
        JOIN Film_Piattaforma ON Film.id = Film_Piattaforma.film_id
        JOIN Piattaforma ON Piattaforma.id = Film_Piattaforma.piattaforma_id
        WHERE Piattaforma.nome = 'Netflix'
        """
        return sql, RegistaResult, "director"

    elif question == "elenca tutti i film di fantascienza.":
        sql = """
        SELECT Film.id, Film.titolo AS name, Film.anno
        FROM Film
        JOIN Genere ON Film.genere_id = Genere.id
        WHERE Genere.nome = 'Fantascienza'
        """
        return sql, FilmResult, "film"

    elif re.match(ANNI_REGEX, question):
        anni = question.replace("quali film sono stati fatti da un regista di almeno ", "").replace(" anni?", "").strip()
        sql = f"""
        SELECT Film.id, Film.titolo AS name, Film.anno
        FROM Film
        JOIN Regista ON Film.regista_id = Regista.id
        WHERE Regista.eta >= {anni}
        """
        return sql, FilmResult, "film"

    elif question == "quali registi hanno fatto più di un film?":
        sql = """
        SELECT Regista.id, Regista.nome AS name, NULL AS anno
        FROM Regista
        JOIN Film ON Regista.id = Film.regista_id
        GROUP BY Regista.id, Regista.nome
        HAVING COUNT(Film.id) > 1
        """
        return sql, RegistaResult, "director"

    else:
        raise ValueError("Domanda non riconosciuta.")



def parse_data_line(data_line: str) -> Tuple[str, int, str, str, str]:
    """
    Dato una riga 'titolo,anno,regista,genere,piattaforma',
    ritorna i valori splittati e convertiti correttamente.
    """
    parts = [p.strip() for p in data_line.split(",")]
    if len(parts) != 5:
        raise ValueError("Formato della riga non valido. Devono esserci 5 valori separati da virgola.")
    titolo, anno, regista, genere, piattaforma = parts
    return titolo, int(anno), regista, genere, piattaforma


def get_schema_summary(connection) -> list[SchemaColumn]:
    """
    Restituisce lo schema del database: una lista di SchemaColumn con table_name e column_name.
    """
    cursor = connection.cursor()
    cursor.execute("""
        SELECT table_name, column_name
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
    """)
    results = cursor.fetchall()
    return [SchemaColumn(table_name=table, column_name=column) for table, column in results]

def importa_film_da_tsv(path, db):
    df = pd.read_csv(path, sep="\t", header=None)
    df.columns = ["Titolo", "Regista", "Età_Autore", "Anno", "Genere", "Piattaforma_1", "Piattaforma_2"]

    for i, row in df.iterrows():
        try:
            piattaforme = []
            if pd.notna(row["Piattaforma_1"]):
                piattaforme.append(row["Piattaforma_1"])
            if pd.notna(row["Piattaforma_2"]):
                piattaforme.append(row["Piattaforma_2"])

            film_data = FilmInput(
                Titolo=row["Titolo"],
                Regista=row["Regista"],
                Età_Autore=int(row["Età_Autore"]),
                Anno=int(row["Anno"]),
                Genere=row["Genere"],
                Piattaforme=piattaforme
            )

            # === Inserimento in ordine referenziale ===
            # REGISTA
            regista = db.query(Regista).filter_by(nome=film_data.Regista).first()
            if not regista:
                regista = Regista(nome=film_data.Regista, eta=film_data.Età_Autore)
                db.add(regista)
                db.flush()

            # GENERE
            genere = db.query(Genere).filter_by(nome=film_data.Genere).first()
            if not genere:
                genere = Genere(nome=film_data.Genere)
                db.add(genere)
                db.flush()

            # PIATTAFORME
            piattaforme_ids = []
            for nome_piattaforma in film_data.Piattaforme:
                piattaforma = db.query(Piattaforma).filter_by(nome=nome_piattaforma).first()
                if not piattaforma:
                    piattaforma = Piattaforma(nome=nome_piattaforma)
                    db.add(piattaforma)
                    db.flush()
                piattaforme_ids.append(piattaforma.id)

            # FILM
            film_esistente = db.query(Film).filter_by(titolo=film_data.Titolo, anno=film_data.Anno).first()
            if film_esistente:
                print(f"Film già esistente: {film_data.Titolo} ({film_data.Anno})")
                continue
            
            film = Film(
                titolo=film_data.Titolo,
                anno=film_data.Anno,
                regista_id=regista.id,
                genere_id=genere.id
            )
            db.add(film)
            db.flush()

            # FILM_PIATTAFORMA
            for pid in piattaforme_ids:
                db.add(FilmPiattaforma(film_id=film.id, piattaforma_id=pid))

            print(f"[✓] {film.titolo} inserito.")
        except ValidationError as ve:
            print(f"[!] Errore validazione riga {i+1}: {ve}")
        except Exception as e:
            print(f"[!] Errore generale riga {i+1}: {e}")

    db.commit()

def importa_film_da_csv(data: CSVInput, db):
    try:
        reader = csv.DictReader(StringIO(data.contenuto), delimiter=",")

        for row in reader:
            row = {k: v.rstrip(',') if isinstance(v, str) else v for k, v in row.items()}

            # REGISTA
            regista = db.query(Regista).filter_by(nome=row["Regista"]).first()
            if not regista:
                regista = Regista(nome=row["Regista"], eta=int(row["Età_Autore"]))
                db.add(regista)
                db.flush()

            # GENERE
            genere = db.query(Genere).filter_by(nome=row["Genere"]).first()
            if not genere:
                genere = Genere(nome=row["Genere"])
                db.add(genere)
                db.flush()

            # FILM (controllo duplicati)
            film_esistente = db.query(Film).filter_by(
                titolo=row["Titolo"], anno=int(row["Anno"])
            ).first()
            if film_esistente:
                continue

            film = Film(
                titolo=row["Titolo"],
                anno=int(row["Anno"]),
                regista_id=regista.id,
                genere_id=genere.id
            )
            db.add(film)
            db.flush()

            # PIATTAFORME
            for key in ["Piattaforma_1", "Piattaforma_2"]:
                nome_piattaforma = row.get(key)
                if nome_piattaforma:
                    piattaforma = db.query(Piattaforma).filter_by(nome=nome_piattaforma).first()
                    if not piattaforma:
                        piattaforma = Piattaforma(nome=nome_piattaforma)
                        db.add(piattaforma)
                        db.flush()

                    # Associazione film - piattaforma
                    esiste_associazione = db.query(FilmPiattaforma).filter_by(
                        film_id=film.id, piattaforma_id=piattaforma.id
                    ).first()
                    if not esiste_associazione:
                        db.add(FilmPiattaforma(film_id=film.id, piattaforma_id=piattaforma.id))

        db.commit()
        return {"status": "ok"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=200, detail=str(e))