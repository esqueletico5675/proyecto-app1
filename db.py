import os
from pathlib import Path
from dotenv import load_dotenv
from sqlmodel import Session, create_engine, SQLModel
from fastapi import FastAPI, Depends
from typing import Annotated
from models import *

load_dotenv()
neon_db = os.getenv("DATABASE_URL")
print("DB URL;", neon_db)
engine = create_engine(neon_db)

def create_all_tables(app: FastAPI):
    print("Creando tablas...")
    SQLModel.metadata.create_all(engine)
    print("Tablas creadas!")
    yield

def get_session() -> Session:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]




SessionDep = Annotated[Session, Depends(get_session)]