from typing import Tuple
from schemas import FilmResult, RegistaResult, FilmConRegistaEtaResult, RegistaMultiFilmResult, SchemaColumn
import re

ANNO_REGEX = r"^elenca i film del (\d{4})\.$"
ANNI_REGEX = r"^quali film sono stati fatti da un regista di almeno (\d+) anni\?$"

def match_question_to_sql(question: str) -> Tuple[str, type]:
    """
    Dato una domanda letterale, ritorna:
    - la query SQL corrispondente
    - lo schema Pydantic da usare come output
    """
    question = question.lower().strip()
    print(question)

    if re.match(ANNO_REGEX, question):
        anno = question.replace("elenca i film del ", "").replace(".", "").strip()
        sql = f"""
        SELECT titolo, anno 
        FROM Film 
        WHERE anno = {anno}
        """
        return sql, FilmResult

    elif question == "quali sono i registi presenti su netflix?":
        sql = """
        SELECT DISTINCT Regista.nome
        FROM Regista
        JOIN Film ON Film.regista_id = Regista.id
        JOIN Film_Piattaforma ON Film.id = Film_Piattaforma.film_id
        JOIN Piattaforma ON Piattaforma.id = Film_Piattaforma.piattaforma_id
        WHERE Piattaforma.nome = 'Netflix'
        """
        return sql, RegistaResult

    elif question == "elenca tutti i film di fantascienza.":
        sql = """
        SELECT Film.titolo, Film.anno
        FROM Film
        JOIN Genere ON Film.genere_id = Genere.id
        WHERE Genere.nome ILIKE 'Fantascienza'
        """
        return sql, FilmResult

    elif re.match(ANNI_REGEX, question):
        anni = question.replace("quali film sono stati fatti da un regista di almeno ", "").replace(" anni?", "").strip()
        sql = f"""
        SELECT Film.titolo, Regista.nome AS regista, Regista.eta
        FROM Film
        JOIN Regista ON Film.regista_id = Regista.id
        WHERE Regista.eta >= {anni}
        """
        return sql, FilmConRegistaEtaResult

    elif question == "quali registi hanno fatto più di un film?":
        sql = """
        SELECT Regista.nome, COUNT(Film.id) AS numero_film
        FROM Regista
        JOIN Film ON Regista.id = Film.regista_id
        GROUP BY Regista.nome
        HAVING COUNT(Film.id) > 1
        """
        return sql, RegistaMultiFilmResult

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
