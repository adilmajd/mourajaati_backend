from fastapi import APIRouter,Depends
from data.user import add_permission, add_role, add_user, assign_permission_to_role, assign_role_to_user, change_user_etat, delete_permission, delete_role, delete_user, get_all_permissions, get_all_roles, get_all_user, get_permission_by_id, get_role_by_id, get_user_by_mail, get_user_by_nom, remove_role_from_user, update_permission, update_role, update_user
from database.base import get_session
from sqlmodel import Session, select

from model.User import Permission, Role, User
"""
end point (les APIs) des Users
/ -> gestion des utilisateurs.

/roles/ -> gestion des rôles & affectation aux utilisateurs.

/permissions/ -> gestion des permissions & affectation aux rôles.
"""


router = APIRouter()

# ======================
# Gestion Utilisateurs
# ======================


@router.get("/all/")
async def get_all_user_read(session: Session = Depends(get_session)):
     return get_all_user(session)

@router.get("/nom/{nom}")
async def get_user_by_nom_read(nom: str,session: Session = Depends(get_session)):
     return get_user_by_nom(session,nom)

@router.get("/mail/{mail}")
async def get_user_by_mail_read(mail: str,session: Session = Depends(get_session)):
     return get_user_by_mail(session,mail)

@router.post("/")
def add_user_read(user: User, session: Session = Depends(get_session)):
    return add_user(session, user)

@router.put("/{user_id}")
def update_user_read(user_id: int, updates: dict, session: Session = Depends(get_session)):
    return update_user(session, user_id, updates)

@router.delete("/{user_id}")
def delete_user_read(user_id: int, session: Session = Depends(get_session)):
    return delete_user(session, user_id)

@router.put("/{user_id}/etat/{etat_id}")
def change_user_etat_read(user_id: int, etat_id: int, session: Session = Depends(get_session)):
    return change_user_etat(session, user_id, etat_id)

# ======================
# Gestion Rôle & Permissions
# ======================


# Rôles

@router.get("/roles/")
def get_all_roles_read(session: Session = Depends(get_session)):
    return get_all_roles(session)

@router.get("/roles/{role_id}")
def get_role_by_id_read(role_id: int, session: Session = Depends(get_session)):
    return get_role_by_id(session, role_id)

@router.post("/roles/")
def add_role_read(role: Role, session: Session = Depends(get_session)):
    return add_role(session, role)

@router.post("/roles/{role_id}/users/{user_id}")
def assign_role_to_user_read(role_id: int, user_id: int, session: Session = Depends(get_session)):
    return assign_role_to_user(session, user_id, role_id)

@router.delete("/roles/{role_id}/users/{user_id}")
def remove_role_from_user_read(role_id: int, user_id: int, session: Session = Depends(get_session)):
    return remove_role_from_user(session, user_id, role_id)

@router.put("/roles/{role_id}")
def update_role_read(role_id: int, updates: dict, session: Session = Depends(get_session)):
    return update_role(session, role_id, updates)

@router.delete("/roles/{role_id}")
def delete_role_read(role_id: int, session: Session = Depends(get_session)):
    return delete_role(session, role_id)

# Permissions

@router.get("/permissions/")
def get_all_permissions_read(session: Session = Depends(get_session)):
    return get_all_permissions(session)

@router.get("/permissions/{permission_id}")
def get_permission_by_id_read(permission_id: int, session: Session = Depends(get_session)):
    return get_permission_by_id(session, permission_id)

@router.post("/permissions/")
def add_permission_permission(permission: Permission, session: Session = Depends(get_session)):
    return add_permission(session, permission)

@router.post("/permissions/{permission_id}/roles/{role_id}")
def assign_permission_to_role_read(permission_id: int, role_id: int, session: Session = Depends(get_session)):
    return assign_permission_to_role(session, role_id, permission_id)

@router.put("/permissions/{permission_id}")
def update_permission_read(permission_id: int, updates: dict, session: Session = Depends(get_session)):
    return update_permission(session, permission_id, updates)

@router.delete("/permissions/{permission_id}")
def delete_permission_read(permission_id: int, session: Session = Depends(get_session)):
    return delete_permission(session, permission_id)