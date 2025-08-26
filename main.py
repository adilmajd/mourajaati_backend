# main.py

from typing import Annotated,Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

from model.Base import Ville


DATABASE_URL = "mysql+pymysql://root:1234@localhost:3306/mourajaati"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session



app = FastAPI()

@app.get("/ville/", response_model=list[Ville])
def read_users(session: Session = Depends(get_session)):
    villes = session.exec(select(Ville)).all()
    return villes

@app.get("/")
async def read_root():
    return {"message": "Master it 2024 2025"}