from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator

DB_USER = "root"
DB_PASSWORD = "rootpassword"
DB_HOST = "localhost"
DB_PORT = "3307"
DB_NAME = "esonero"

DATABASE_URL = "mysql+pymysql://{}:{}@{}:{}/{}".format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def execute_sql(db, query: str):
    result = db.execute(text(query))
    return result.fetchall()

def get_schema_summary(connection):
    schema = []
    database_name = "esonero"

    # Recupera tutte le tabelle del database specificato
    tables = connection.execute(
        text(f"SELECT table_name FROM information_schema.tables WHERE table_schema = :database_name AND table_type = 'BASE TABLE';"),
        {'database_name': database_name}
    )

    for table in tables:
        table_name = table[0]
        
        # Recupera tutte le colonne per ciascuna tabella
        columns = connection.execute(
            text(f"SELECT column_name FROM information_schema.columns WHERE table_schema = :database_name AND table_name = :table_name;"),
            {'database_name': database_name, 'table_name': table_name}
        )

        # Crea una lista di colonne come stringa separata da virgole
        column_names = [column[0] for column in columns]
        columns_str = ', '.join(column_names)  # Unisce i nomi delle colonne con virgole
        
        # Aggiungi il nome della tabella e le colonne come stringa al risultato
        schema.append(f"{table_name}: {columns_str}")
    
    return schema
