
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db, execute_sql, get_schema_summary
from typing import Dict
from utils import match_question_to_sql

app = FastAPI()

domande = ["Elenca i film del <ANNO>.", "Quali sono i registi presenti su Netflix?", "Elenca tutti i film di fantascienza.", "Quali film sono stati fatti da un regista di almeno <ANNI> anni?", "Quali registi hanno fatto più di un film?" ]

@app.get("/search")
def search(question: str, db: Session = Depends(get_db)):
    try:
        sql, schema = match_question_to_sql(question)
        
        result = execute_sql(db, sql)
        return [schema(**dict(row)) for row in result]
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            'errore': str(e),
            'possibiili domande': domande
        })
    
    

@app.get("/schema_summary")
def schema_summary(db: Session = Depends(get_db)):
    
    return get_schema_summary(db.connection())

@app.post("/add")

async def process_data(data: Dict[str, str]):

    # Verifica che l'attributo "data_line" sia presente nel dizionario
    data_line = data.get("data_line")

    if not data_line:  # Se "data_line" non è presente o è vuoto
        raise HTTPException(status_code=400, detail="'data_line' mancante nella richiesta.")

    # Restituisci un dizionario con la stessa chiave e valore ricevuto
    return {"data_line": data_line}

