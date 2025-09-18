
from fastapi import HTTPException
from sqlmodel import Session, select

from model.Autre import UpdateUserNiveau
from model.Base import Cycle, Niveau
from model.User import User


def get_user_niveau(user_public_id: str, session: Session):
    # Récupération de l'utilisateur
    user = session.exec(select(User).where(User.user_public_id == user_public_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Récupération du niveau associé
    niveau = session.get(Niveau, user.niveau_id)
    if not niveau:
        raise HTTPException(status_code=404, detail="Niveau non trouvé")

    # ⚠️ Retourne bien un objet SQLModel
    return niveau

def get_niveaux_by_cycle(cycle_id: int, session: Session):
    cycle = session.get(Cycle, cycle_id)
    if not cycle:
        raise HTTPException(404, "Cycle non trouvé")

    # récupérer les niveaux associés
    niveaux = session.exec(select(Niveau).where(Niveau.cycle_id == cycle_id).order_by(Niveau.order)).all()
    return niveaux

def update_user_niveau(user_public_id: str, payload: UpdateUserNiveau, session: Session):
    # Récupérer l'utilisateur
    user = session.exec(select(User).where(User.user_public_id == user_public_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    # Vérifier que le niveau existe
    niveau = session.get(Niveau, payload.niveau_id)
    if not niveau:
        raise HTTPException(status_code=404, detail="Niveau non trouvé")
    
    # Mettre à jour le niveau de l'utilisateur
    user.niveau_id = payload.niveau_id
    session.add(user)
    session.commit()
    session.refresh(user)

    return {"message": "Niveau utilisateur mis à jour", "niveau_id": user.niveau_id}