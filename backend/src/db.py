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
    tables = connection.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    for table in tables:
        table_name = table[0]
        columns = connection.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
        for column in columns:
            schema.append({"table_name": table_name, "column_name": column[0]})
    return schema