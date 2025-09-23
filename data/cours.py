from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from model.Autre import CoursCreate, CoursRead, CoursUpdate, NiveauRead, TypeCoursRead
from model.Base import Niveau
from model.Cours import Comment, Cours, Exercice, Post, Typecours, UserExercice  # ton fichier connexion DB

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


def delete_cours_post_exercice(cours_id: int, session: Session):
    cours = session.get(Cours, cours_id)
    if not cours:
        raise HTTPException(status_code=404, detail="Cours introuvable")
    
    # 1. Supprimer les exercices et user_exercice
    exercices = session.exec(select(Exercice).where(Exercice.cours_id == cours_id)).all()
    for ex in exercices:
        # supprimer UserExercice lié
        user_exs = session.exec(select(UserExercice).where(UserExercice.exercice_id == ex.exercice_id)).all()
        for ue in user_exs:
            session.delete(ue)
        session.delete(ex)

    # 2. Supprimer les posts et commentaires
    posts = session.exec(select(Post).where(Post.cours_id == cours_id)).all()
    for post in posts:
        comments = session.exec(select(Comment).where(Comment.post_id == post.post_id)).all()
        for com in comments:
            session.delete(com)
        session.delete(post)

    # 3. Supprimer le cours
    session.delete(cours)
    session.commit()
    
    return {"message": "Cours et tous les contenus liés supprimés avec succès"}

def add_cours(cours: CoursCreate, session: Session):
    new_cours = Cours(
        cours_titre=cours.cours_titre,
        niveau_id=cours.niveau_id,
        type_cours_id=cours.type_cours_id,
        user_id=1  # ou le user connecté
    )
    session.add(new_cours)
    session.commit()
    session.refresh(new_cours)
    return {"message": "Cours ajouté avec succès", "cours": new_cours}