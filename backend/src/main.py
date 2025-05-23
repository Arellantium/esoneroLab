
from fastapi import FastAPI, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from db import get_db, execute_sql, get_schema_summary
from typing import Dict
from utils import match_question_to_sql, importa_film_da_tsv, importa_film_da_csv
from schemas import CSVInput
from fastapi.middleware.cors import CORSMiddleware
from tenacity import retry, stop_after_attempt, wait_fixed
import time
from sqlalchemy import text

@retry(stop=stop_after_attempt(10), wait=wait_fixed(2))
def wait_for_db():
    print("⏳ Aspetto che MariaDB sia pronto...")
    db = next(get_db())
    db.execute(text("SELECT 1"))
    print("✅ MariaDB pronto.")


path = "data.tsv"

@asynccontextmanager
async def lifespan(app: FastAPI):
    wait_for_db()
    try:
        print("ciao")
        db = next(get_db())  
        importa_film_da_tsv(path, db)
    except FileNotFoundError:
        print(" File TSV non trovato.")
    
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ATTENZIONE: in produzione meglio specificare!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

domande = ["Elenca i film del <ANNO>.", "Quali sono i registi presenti su Netflix?", "Elenca tutti i film di fantascienza.", "Quali film sono stati fatti da un regista di almeno <ANNI> anni?", "Quali registi hanno fatto più di un film?" ]



@app.get("/search/{question}")
def search(question: str, db: Session = Depends(get_db)):
    try:
        sql, schema, item_type = match_question_to_sql(question)
        result = execute_sql(db, sql)

        response = []
        for row in result:
            item = schema(**row) 

            properties = []

            for field_name, field_value in item.model_dump().items():
                prop_name = "name" if field_name in ["titolo", "nome"] else field_name

                
                if isinstance(field_value, str) and field_name in ["id", "anno", "eta", "numero_film"]:
                    try:
                        field_value = int(field_value)
                    except:
                        pass

                properties.append({
                    "property_name": prop_name,
                    "property_value": field_value
                })

            response.append({
                "item_type": item_type,
                "properties": properties
            })

        return response

    except Exception as e:
        status_code = 422 if "Domanda non riconosciuta" in str(e) else 400
        raise HTTPException(status_code=status_code, detail={
            "errore": "Domanda non riconosciuta, possibili domande: ",
            "possibili_domande": domande
        })


 

@app.get("/schema_summary")
def schema_summary(db: Session = Depends(get_db)):
    try:
        return get_schema_summary(db.connection())
    except Exception as e:
        status_code = 200 if "Domanda non riconosciuta" in str(e) else 200
        raise HTTPException(status_code=status_code, detail={
            "errore": str(e)
        })
    

@app.get("/inserimento_tsv")

async def lettura( db: Session =Depends(get_db)):
    importa_film_da_tsv(path, db)
   

@app.post("/add")
async def process_data(form_data: CSVInput , db: Session = Depends(get_db)):
    try:
        print("entrato")
        importa_film_da_csv(form_data, db)
        return {"status": "ok"}
    except Exception as e:
        print("ingresso eccezione")
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
            "errore": str(e)
        })
