# main.py

from typing import Annotated,Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, select

from database.base import get_session
from model.Base import Ville





app = FastAPI()

@app.get("/ville/", response_model=list[Ville])
def read_users(session: Session = Depends(get_session)):
    villes = session.exec(select(Ville)).all()
    return villes

@app.get("/")
async def read_root():
    return {"message": "Master it 2024 2025"}