from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator

DB_USER = "root"
DB_PASSWORD = "rootpassword"
#DB_HOST = "localhost"
DB_HOST = "host.docker.internal"
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
    print(query)
    result = db.execute(text(query))
    
    rows = result.fetchall()
    keys = result.keys()

    # Costruisce dizionari con conversione dei tipi forzata
    final_result = []
    for row in rows:
        row_dict = dict(zip(keys, row))
        # Prova a convertire eventuali interi esplicitamente
        for k, v in row_dict.items():
            if k in ['id', 'anno', 'eta', 'numero_film'] and isinstance(v, str):
                try:
                    row_dict[k] = int(v)
                except:
                    pass  # fallback in caso sia già int o non convertibile
        final_result.append(row_dict)
        print(final_result)

    return final_result

def get_schema_summary(connection):
    schema = []
    database_name = "esonero"
    
    # Prendi tutte le tabelle del database
    tables = connection.execute(
        text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = :database_name AND table_type = 'BASE TABLE';
        """),
        {'database_name': database_name}
    )

    for table in tables:
        table_name = table[0]

        # Prendi tutte le colonne con dettagli
        columns = connection.execute(
            text("""
                SELECT 
                    col.column_name,
                    col.data_type,
                    col.is_nullable,
                    col.column_default,
                    tc.constraint_type,
                    kcu.referenced_table_name,
                    kcu.referenced_column_name
                FROM information_schema.columns col
                LEFT JOIN information_schema.key_column_usage kcu
                    ON col.table_name = kcu.table_name
                    AND col.column_name = kcu.column_name
                    AND col.table_schema = kcu.table_schema
                LEFT JOIN information_schema.table_constraints tc
                    ON kcu.constraint_name = tc.constraint_name
                    AND kcu.table_name = tc.table_name
                    AND kcu.table_schema = tc.table_schema
                WHERE col.table_schema = :database_name AND col.table_name = :table_name;
            """),
            {'database_name': database_name, 'table_name': table_name}
        )

        for col in columns:
            column_info = {
                "table_name": {
        "Film": "movies",
        "Regista": "directors",
        "Genere": "genres",
        "Piattaforma": "platforms",
        "Film_Piattaforma": "movie_platforms"
    }.get(table_name, table_name),
                "column_name": col.column_name,
                "table_column": f"{table_name}.{col.column_name}"
              #  "data_type": col.data_type,
              #  "is_nullable": col.is_nullable,
               # "default": col.column_default,
                #"is_primary": col.constraint_type == 'PRIMARY KEY',
                #"is_foreign": col.constraint_type == 'FOREIGN KEY',
                #"references": f"{col.referenced_table_name}.{col.referenced_column_name}" if col.constraint_type == 'FOREIGN KEY' else None
            }
            schema.append(column_info)

    return schema
