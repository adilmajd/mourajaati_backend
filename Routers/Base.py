from fastapi import APIRouter,Depends
from data.CRUD import create_entity, delete_entity, get_all_entities, get_entity_by_id, update_entity
from data.base import get_niveaux_by_cycle, get_user_niveau
from database.base import get_session
from sqlmodel import Session, select
from typing import List, Optional
from model.Autre import NiveauRead
from model.Base import CodePostale, Ecole, Cycle, Niveau, Ville

"""

"""


router = APIRouter()

@router.get("/user/{user_public_id}/niveau", response_model=Niveau)
def get_user_niveau_r(user_public_id: str, session: Session = Depends(get_session)):
    return get_user_niveau(user_public_id,session)


@router.get("/cycles/{cycle_id}/niveaux", response_model=List[NiveauRead])
def get_niveaux_by_cycle_r(cycle_id: int, session: Session = Depends(get_session)):
    return get_niveaux_by_cycle(cycle_id,session)
   








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


# ---- Cycle ---- cycle
@router.post("/cycles/", response_model=Cycle)
def add_niveau(cycle: Cycle, session: Session = Depends(get_session)):
    return create_entity(session, cycle)

@router.get("/cycles/", response_model=List[Cycle])
def list_niveaux(cycle: Session = Depends(get_session)):
    return get_all_entities(cycle, Cycle)


# ---- ECOLE ----
@router.post("/ecoles/", response_model=Ecole)
def add_ecole(ecole: Ecole, session: Session = Depends(get_session)):
    return create_entity(session, ecole)

@router.get("/ecoles/", response_model=List[Ecole])
def list_ecoles(session: Session = Depends(get_session)):
    return get_all_entities(session, Ecole)


# ---- GRADE ----
@router.post("/niveaux/", response_model=Niveau)
def add_grade(niveau: Niveau, session: Session = Depends(get_session)):
    return create_entity(session, niveau)

@router.get("/niveaux/", response_model=List[Niveau])
def list_grades(session: Session = Depends(get_session)):
    return get_all_entities(session, Niveau)