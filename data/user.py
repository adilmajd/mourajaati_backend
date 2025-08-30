from fastapi import HTTPException
from model.User import User
from sqlmodel import Session, select


def get_all_user(session: Session):
    users = session.exec(select(User)).all()
    return users

def add_user(session: Session, user: User):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def update_user(session: Session, user_id: int, updates: dict):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404, "Utilisateur non trouvé")
    for key, value in updates.items():
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def delete_user(session: Session, user_id: int):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404, "Utilisateur non trouvé")
    session.delete(user)
    session.commit()
    return {"message": "Utilisateur supprimé"}

def get_user_by_nom(session: Session, nom: str):
    return session.exec(select(User).where(User.nom == nom)).all()

def get_user_by_mail(session: Session, mail: str):
    return session.exec(select(User).where(User.mail == mail)).first()

def get_user_by_etat(session: Session, etat_id: int):
    return session.exec(select(User).where(User.etat_id == etat_id)).all()
