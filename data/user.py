from fastapi import HTTPException
from model.User import Permission, Role, RoleHasPermission, User, UserHasRole
from sqlmodel import Session, select

"""
Gestion des utilisateurs (ajout, modification, suppression, recherche).

Gestion des rôles (ajout, suppression, affectation utilisateur,modification).

Gestion des permissions (ajout, suppression, affectation aux rôles,modification).
"""

# ======================
# Gestion Utilisateurs
# ======================

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
def get_all_roles(session: Session):
    return session.exec(select(Role)).all()

def get_role_by_id(session: Session, role_id: int):
    role = session.get(Role, role_id)
    if not role:
        raise HTTPException(404, "Rôle non trouvé")
    return role

def add_role(session: Session, role: Role):
    session.add(role)
    session.commit()
    session.refresh(role)
    return role

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

def update_role(session: Session, role_id: int, updates: dict):
    role = session.get(Role, role_id)
    if not role:
        raise HTTPException(404, "Rôle non trouvé")
    for key, value in updates.items():
        setattr(role, key, value)
    session.add(role)
    session.commit()
    session.refresh(role)
    return role

def delete_role(session: Session, role_id: int):
    role = session.get(Role, role_id)
    if not role:
        raise HTTPException(404, "Rôle non trouvé")
    session.delete(role)
    session.commit()
    return {"message": f"Rôle {role_id} supprimé avec succès"}

# ---- PERMISSIONS ----
def get_all_permissions(session: Session):
    return session.exec(select(Permission)).all()

def get_permission_by_id(session: Session, permission_id: int):
    permission = session.get(Permission, permission_id)
    if not permission:
        raise HTTPException(404, "Permission non trouvée")
    return permission

def add_permission(session: Session, permission: Permission):
    session.add(permission)
    session.commit()
    session.refresh(permission)
    return permission

def assign_permission_to_role(session: Session, role_id: int, permission_id: int):
    link = RoleHasPermission(role_id=role_id, permission_id=permission_id)
    session.add(link)
    session.commit()
    return {"message": "Permission assignée"}


def update_permission(session: Session, permission_id: int, updates: dict):
    permission = session.get(Permission, permission_id)
    if not permission:
        raise HTTPException(404, "Permission non trouvée")
    for key, value in updates.items():
        setattr(permission, key, value)
    session.add(permission)
    session.commit()
    session.refresh(permission)
    return permission

def delete_permission(session: Session, permission_id: int):
    permission = session.get(Permission, permission_id)
    if not permission:
        raise HTTPException(404, "Permission non trouvée")
    session.delete(permission)
    session.commit()
    return {"message": f"Permission {permission_id} supprimée avec succès"}