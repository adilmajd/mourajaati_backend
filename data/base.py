
from fastapi import HTTPException
from sqlmodel import Session, select

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