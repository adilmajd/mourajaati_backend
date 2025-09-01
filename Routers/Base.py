from fastapi import APIRouter,Depends
from data.CRUD import create_entity, delete_entity, get_all_entities, get_entity_by_id, update_entity
from database.base import get_session
from sqlmodel import Session, select
from typing import List, Optional
from model.Base import CodePostale, Ecole, Grade, Niveau, Ville

"""

"""


router = APIRouter()

# ---- VILLE ----
@router.post("/villes/", response_model=Ville)
def add_ville(ville: Ville, session: Session = Depends(get_session)):
    return create_entity(session, ville)

@router.get("/villes/", response_model=List[Ville])
def list_villes(session: Session = Depends(get_session)):
    return get_all_entities(session, Ville)

@router.get("/villes/{ville_id}", response_model=Ville)
def get_ville(ville_id: int, session: Session = Depends(get_session)):
    return get_entity_by_id(session, Ville, ville_id)

@router.put("/villes/{ville_id}", response_model=Ville)
def update_ville(ville_id: int, updates: dict, session: Session = Depends(get_session)):
    return update_entity(session, Ville, ville_id, updates)

@router.delete("/villes/{ville_id}")
def remove_ville(ville_id: int, session: Session = Depends(get_session)):
    return delete_entity(session, Ville, ville_id)


# ---- CODE POSTALE ----
@router.post("/codes_postaux/", response_model=CodePostale)
def add_cp(cp: CodePostale, session: Session = Depends(get_session)):
    return create_entity(session, cp)

@router.get("/codes_postaux/", response_model=List[CodePostale])
def list_cp(session: Session = Depends(get_session)):
    return get_all_entities(session, CodePostale)


# ---- NIVEAU ----
@router.post("/niveaux/", response_model=Niveau)
def add_niveau(niveau: Niveau, session: Session = Depends(get_session)):
    return create_entity(session, niveau)

@router.get("/niveaux/", response_model=List[Niveau])
def list_niveaux(session: Session = Depends(get_session)):
    return get_all_entities(session, Niveau)


# ---- ECOLE ----
@router.post("/ecoles/", response_model=Ecole)
def add_ecole(ecole: Ecole, session: Session = Depends(get_session)):
    return create_entity(session, ecole)

@router.get("/ecoles/", response_model=List[Ecole])
def list_ecoles(session: Session = Depends(get_session)):
    return get_all_entities(session, Ecole)


# ---- GRADE ----
@router.post("/grades/", response_model=Grade)
def add_grade(grade: Grade, session: Session = Depends(get_session)):
    return create_entity(session, grade)

@router.get("/grades/", response_model=List[Grade])
def list_grades(session: Session = Depends(get_session)):
    return get_all_entities(session, Grade)