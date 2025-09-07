from fastapi import HTTPException
from model.User import Permission, Role, RoleHasPermission, User, UserHasRole
from sqlmodel import Session, select

"""

"""

# ======================
# Gestion Utilisateurs
# ======================

#fonction d'authentification
def login_user(session: Session,login: str,compte_password: str):
    statement=(
            select(User)
               .where(User.login==login)
               .where(User.compte_password == compte_password)
               .where(User.etat_id == 1)
               )
    result = session.exec(statement).first()
    if not result:
        return None
    return result

def get_user_by_mail(session: Session, mail: str):
    return session.exec(select(User).where(User.mail == mail)).first()

def get_user_by_etat(session: Session, etat_id: int):
    return session.exec(select(User).where(User.etat_id == etat_id)).all()

def change_user_etat(session: Session, user_id: int, etat_id: int):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404, "Utilisateur non trouvé")
    user.etat_id = etat_id
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# ======================
# Gestion Rôle & Permissions
# ======================

# ---- RÔLES ----

def assign_role_to_user(session: Session, user_id: int, role_id: int):
    link = UserHasRole(user_id=user_id, role_id=role_id)
    session.add(link)
    session.commit()
    return {"message": "Rôle assigné"}

def remove_role_from_user(session: Session, user_id: int, role_id: int):
    link = session.get(UserHasRole, (user_id, role_id))
    if not link:
        raise HTTPException(404, "Lien non trouvé")
    session.delete(link)
    session.commit()
    return {"message": "Rôle retiré"}


# ---- PERMISSIONS ----


def assign_permission_to_role(session: Session, role_id: int, permission_id: int):
    link = RoleHasPermission(role_id=role_id, permission_id=permission_id)
    session.add(link)
    session.commit()
    return {"message": "Permission assignée"}


