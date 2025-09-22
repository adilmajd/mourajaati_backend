from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from model.Autre import CoursRead, CoursUpdate, NiveauRead, TypeCoursRead
from model.Base import Niveau
from model.Cours import Cours, Typecours  # ton fichier connexion DB

def list_cours_nv_type(session: Session):
    statement = (
        select(Cours, Niveau, Typecours)
        .join(Niveau, Cours.niveau_id == Niveau.niveau_id)
        .join(Typecours, Cours.type_cours_id == Typecours.type_cours_id)
    )
    results = session.exec(statement).all()

    cours_list = []
    for cours, niveau, type_cours in results:
        cours_list.append(CoursRead(
            cours_id=cours.cours_id,
            cours_titre=cours.cours_titre,
            niveau=NiveauRead.from_orm(niveau),
            type_cours=TypeCoursRead.from_orm(type_cours)
        ))
    return cours_list



def update_cours_nv_type(cours_id: int, data: CoursUpdate, session: Session):
    cours = session.get(Cours, cours_id)
    if not cours:
        raise HTTPException(404, "Cours introuvable")
    
    cours.niveau_id = data.niveau_id
    cours.type_cours_id = data.type_cours_id
    session.add(cours)
    session.commit()
    session.refresh(cours)

    niveau = session.get(Niveau, cours.niveau_id)
    type_cours = session.get(Typecours, cours.type_cours_id)

    return CoursRead(
        cours_id=cours.cours_id,
        cours_titre=cours.cours_titre,
        niveau=niveau,
        type_cours=type_cours
    )