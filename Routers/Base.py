from fastapi import APIRouter,Depends
from data.CRUD import create_entity, delete_entity, get_all_entities, get_entity_by_id, update_entity
from data.base import get_niveaux_by_cycle, get_user_niveau, update_user_niveau
from data.user import require_permission, require_role
from database.base import get_session
from sqlmodel import Session, select
from typing import List, Optional
from model.Autre import NiveauRead, UpdateUserNiveau
from model.Base import Cycle, Niveau

"""

"""


router = APIRouter()

@router.get("/user/{user_public_id}/niveau", response_model=Niveau)
def get_user_niveau_r(user_public_id: str, session: Session = Depends(get_session)):
    return get_user_niveau(user_public_id,session)


@router.get("/cycles/{cycle_id}/niveaux", response_model=List[NiveauRead])
def get_niveaux_by_cycle_r(cycle_id: int, session: Session = Depends(get_session)):
    return get_niveaux_by_cycle(cycle_id,session)
   

@router.put("/user/{user_public_id}/niveau")
def update_user_niveau_r(user_public_id: str, payload: UpdateUserNiveau, session: Session = Depends(get_session)):
    return update_user_niveau(user_public_id,payload,session)
    







# ---- Cycle ---- cycle
@router.post("/cycles/", response_model=Cycle)
def add_niveau(cycle: Cycle, session: Session = Depends(get_session)):
    return create_entity(session, cycle)

@router.get("/cycles/", response_model=List[Cycle])
def list_niveaux(cycle: Session = Depends(get_session)):
    return get_all_entities(cycle, Cycle)




# ---- GRADE ----
@router.post("/niveaux/", response_model=Niveau)
def add_grade(niveau: Niveau, session: Session = Depends(get_session)):
    return create_entity(session, niveau)

@router.get("/niveaux/", response_model=List[Niveau])
def list_grades(session: Session = Depends(get_session)):
    return get_all_entities(session, Niveau)