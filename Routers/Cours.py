from fastapi import APIRouter,Depends
from data.CRUD import create_entity, delete_entity, get_all_entities, get_entity_by_id, update_entity
from data.cours import add_cours, delete_cours_post_exercice, list_cours_nv_type, update_cours_nv_type
from database.base import get_session
from sqlmodel import Session, select
from typing import List, Optional

from model.Autre import CoursCreate, CoursRead, CoursUpdate, TypeCreate
from model.Cours import Cours, Examen, Exercice, Post, Comment, Typecours, UserExamen, UserExercice

"""

"""


router = APIRouter()

# ---- COURS ----
"""
@router.post("/cour/", response_model=Cours)
def add_cours(cours: Cours, session: Session = Depends(get_session)):
    return create_entity(session, cours)
"""
@router.post("/cour/", response_model=Cours)
def add_cours_r(cours: CoursCreate, session: Session = Depends(get_session)):
    return add_cours(cours,session)

@router.get("/cours/", response_model=List[Cours])
def list_cours(session: Session = Depends(get_session)):
    return get_all_entities(session, Cours)

@router.get("/cours/{cours_id}", response_model=Cours)
def get_cours(cours_id: int, session: Session = Depends(get_session)):
    return get_entity_by_id(session, Cours, cours_id)

@router.put("/cour/{cours_id}", response_model=Cours)
def update_cours(cours_id: int, updates: dict, session: Session = Depends(get_session)):
    return update_entity(session, Cours, cours_id, updates)

"""
@router.delete("/cour/{cours_id}")
def delete_cours(cours_id: int, session: Session = Depends(get_session)):
    return delete_entity(session, Cours, cours_id)
"""
@router.delete("/cour/{cours_id}")
def delete_cours(cours_id: int, session: Session = Depends(get_session)):
    return delete_cours_post_exercice(cours_id,session)



@router.get("/cours_nv_typ/", response_model=List[CoursRead])
def list_cours_nv_type_r(session: Session = Depends(get_session)):
    return list_cours_nv_type(session)

@router.put("/cour/{cours_id}", response_model=CoursRead)
def update_cours_nv_type_r(cours_id: int, data: CoursUpdate, session: Session = Depends(get_session)):
    return update_cours_nv_type(cours_id,data,session)
  

# ---- EXERCICE ----
@router.post("/exercices/", response_model=Exercice)
def add_exercice(exercice: Exercice, session: Session = Depends(get_session)):
    return create_entity(session, exercice)

@router.get("/exercices/", response_model=List[Exercice])
def list_exercices(session: Session = Depends(get_session)):
    return get_all_entities(session, Exercice)


# ---- POST ----
@router.post("/posts/", response_model=Post)
def add_post(post: Post, session: Session = Depends(get_session)):
    return create_entity(session, post)

@router.get("/posts/", response_model=List[Post])
def list_posts(session: Session = Depends(get_session)):
    return get_all_entities(session, Post)


# ---- COMMENT ----
@router.post("/comments/", response_model=Comment)
def add_comment(comment: Comment, session: Session = Depends(get_session)):
    return create_entity(session, comment)

@router.get("/comments/", response_model=List[Comment])
def list_comments(session: Session = Depends(get_session)):
    return get_all_entities(session, Comment)


# ---- EXAMEN ----
@router.post("/examens/", response_model=Examen)
def add_examen(examen: Examen, session: Session = Depends(get_session)):
    return create_entity(session, examen)

@router.get("/examens/", response_model=List[Examen])
def list_examens(session: Session = Depends(get_session)):
    return get_all_entities(session, Examen)


# ---- USER EXAMEN ----
@router.post("/user_examens/", response_model=UserExamen)
def add_user_examen(user_examen: UserExamen, session: Session = Depends(get_session)):
    return create_entity(session, user_examen)

@router.get("/user_examens/", response_model=List[UserExamen])
def list_user_examens(session: Session = Depends(get_session)):
    return get_all_entities(session, UserExamen)


# ---- USER EXERCICE ----
@router.post("/user_exercices/", response_model=UserExercice)
def add_user_exercice(user_exercice: UserExercice, session: Session = Depends(get_session)):
    return create_entity(session, user_exercice)

@router.get("/user_exercices/", response_model=List[UserExercice])
def list_user_exercices(session: Session = Depends(get_session)):
    return get_all_entities(session, UserExercice)


# ---- type ----
@router.post("/type/", response_model=Typecours)
def add_type(type: TypeCreate, session: Session = Depends(get_session)):
    db_type = Typecours(type_cours_nom=type.type_cours_nom)
    return create_entity(session, db_type)


@router.get("/types/", response_model=List[Typecours])
async def list_types(session: Session = Depends(get_session)):
     return get_all_entities(session, Typecours)

@router.put("/type/{type_cours_id}", response_model=Typecours)
def update_role(type_cours_id: int, updates: dict, session: Session = Depends(get_session)):
    return update_entity(session, Typecours, type_cours_id, updates)

@router.delete("/type/{type_cours_id}")
def remove_type(type_cours_id: int, session: Session = Depends(get_session)):
    return delete_entity(session,Typecours,type_cours_id)