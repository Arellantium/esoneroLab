
from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from db import get_db, execute_sql, get_schema_summary
from typing import Dict
from utils import match_question_to_sql, importa_film_da_tsv, importa_film_da_csv

app = FastAPI()

domande = ["Elenca i film del <ANNO>.", "Quali sono i registi presenti su Netflix?", "Elenca tutti i film di fantascienza.", "Quali film sono stati fatti da un regista di almeno <ANNI> anni?", "Quali registi hanno fatto più di un film?" ]
path = "C:\\Users\\aless\Documents\\appunti_univeristari\\EsoneroLab\\data.tsv"



@app.get("/search/{question}")
def search(question: str, db: Session = Depends(get_db)):
    try:
        sql, schema, item_type = match_question_to_sql(question)
        result = execute_sql(db, sql)

        response = []
        for row in result:
            item = schema(**row)  # row è già un dizionario

            properties = []

            for field_name, field_value in item.model_dump().items():
                prop_name = "name" if field_name in ["titolo", "nome"] else field_name

                # Converte a int se il campo è numerico
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
            "errore": str(e),
            "possibili_domande": domande
        })


 

@app.get("/schema_summary")
def schema_summary(db: Session = Depends(get_db)):
    
    return get_schema_summary(db.connection())

@app.get("/inserimento_tsv")

async def lettura( db: Session =Depends(get_db)):
    importa_film_da_tsv(path, db)
   

@app.post("/add")
async def process_data(data, db: Session = Depends(get_db)):
    try:
        importa_film_da_csv(data, db)
    except Exception as e:
        status_code = 200 if "invalid form" in str(e) else 200
        raise HTTPException(status_code=status_code, detail={
            "errore": str(e)
        })
