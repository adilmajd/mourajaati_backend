# main.py

from typing import Annotated,Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, select

from data.user import get_all_user
from database.base import get_session
from model.Base import Ville
from model.User import User





app = FastAPI()

@app.get("/ville/", response_model=list[Ville])
def read_villes(session: Session = Depends(get_session)):
    villes = session.exec(select(Ville)).all()
    return villes

@app.get("/users/", response_model=list[User])
def get_all_users(session: Session = Depends(get_session)):
    return get_all_user(session)

@app.get("/")
async def read_root():
    return {"message": "Master it 2024 2025"}