
from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from db import get_db, execute_sql, get_schema_summary
from typing import Dict
from utils import match_question_to_sql, importa_film_da_tsv, importa_film_da_csv

app = FastAPI()

domande = ["Elenca i film del <ANNO>.", "Quali sono i registi presenti su Netflix?", "Elenca tutti i film di fantascienza.", "Quali film sono stati fatti da un regista di almeno <ANNI> anni?", "Quali registi hanno fatto più di un film?" ]
path = "C:\\Users\\aless\Documents\\appunti_univeristari\\EsoneroLab\\data.tsv"



@app.get("/search")
def search(question: str, db: Session = Depends(get_db)):
    try:
        sql, schema = match_question_to_sql(question)
        
        result = execute_sql(db, sql)
        valori = list({row[0] for row in result})

        return {"risultato": set(valori)}
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            'errore': str(e),
            'possibiili domande': domande
        })
    
    

@app.get("/schema_summary")
def schema_summary(db: Session = Depends(get_db)):
    
    return get_schema_summary(db.connection())

@app.get("/inserimento_tsv")

async def lettura( db: Session =Depends(get_db)):
    importa_film_da_tsv(path, db)
   

@app.post("/add")
async def process_data(data: str = Body(..., media_type="text/plain"), db: Session = Depends(get_db)):
    importa_film_da_csv(data, db)
