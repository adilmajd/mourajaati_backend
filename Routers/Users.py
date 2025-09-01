from fastapi import APIRouter,Depends
from data.CRUD import create_entity, delete_entity, get_all_entities, get_entity_by_id, update_entity
from database.base import get_session
from sqlmodel import Session, select
from typing import List, Optional
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

@router.post("/users/", response_model=User)
def add_user(user: User, session: Session = Depends(get_session)):
    return create_entity(session, User)

@router.get("/users/", response_model=List[User])
async def list_users(session: Session = Depends(get_session)):
     return get_all_entities(session, User)

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int,session: Session = Depends(get_session)):
     return get_entity_by_id(session, User, user_id)

@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updates: dict, session: Session = Depends(get_session)):
    return update_entity(session, User, user_id, updates)

@router.delete("/users/{user_id}")
def remove_user(user_id: int, session: Session = Depends(get_session)):
    return delete_entity(session, User, user_id)
"""
@router.put("/{user_id}/etat/{etat_id}")
def change_user_etat_read(user_id: int, etat_id: int, session: Session = Depends(get_session)):
    return change_user_etat(session, user_id, etat_id)
"""

# ======================
# Gestion Rôle & Permissions
# ======================


# Rôles

@router.post("/roles/", response_model=Role)
def add_role(user: Role, session: Session = Depends(get_session)):
    return create_entity(session, Role)

@router.get("/roles/", response_model=List[Role])
async def list_roles(session: Session = Depends(get_session)):
     return get_all_entities(session, Role)

@router.get("/roles/{role_id}", response_model=Role)
async def get_role(role_id: int,session: Session = Depends(get_session)):
     return get_entity_by_id(session, Role, role_id)

@router.put("/roles/{role_id}", response_model=Role)
def update_role(role_id: int, updates: dict, session: Session = Depends(get_session)):
    return update_entity(session, Role, role_id, updates)

@router.delete("/roles/{role_id}")
def remove_role(role_id: int, session: Session = Depends(get_session)):
    return delete_entity(session, Role, role_id)

"""
@router.post("/roles/{role_id}/users/{user_id}")
def assign_role_to_user_read(role_id: int, user_id: int, session: Session = Depends(get_session)):
    return assign_role_to_user(session, user_id, role_id)

@router.delete("/roles/{role_id}/users/{user_id}")
def remove_role_from_user_read(role_id: int, user_id: int, session: Session = Depends(get_session)):
    return remove_role_from_user(session, user_id, role_id)
"""

# Permissions

@router.post("/permissions/", response_model=Permission)
def add_permission(user: Permission, session: Session = Depends(get_session)):
    return create_entity(session, Permission)

@router.get("/permissions/", response_model=List[Permission])
async def list_permissions(session: Session = Depends(get_session)):
     return get_all_entities(session, Permission)

@router.get("/permissions/{permission_id}", response_model=Permission)
async def get_permission(permission_id: int,session: Session = Depends(get_session)):
     return get_entity_by_id(session, Permission, permission_id)

@router.put("/permissions/{permission_id}", response_model=Permission)
def update_permission(permission_id: int, updates: dict, session: Session = Depends(get_session)):
    return update_entity(session, Permission, permission_id, updates)

@router.delete("/permissions/{permission_id}")
def remove_permission(permission_id: int, session: Session = Depends(get_session)):
    return delete_entity(session, Permission, permission_id)

"""
@router.post("/permissions/{permission_id}/roles/{role_id}")
def assign_permission_to_role_read(permission_id: int, role_id: int, session: Session = Depends(get_session)):
    return assign_permission_to_role(session, role_id, permission_id)


@router.delete("/permissions/{permission_id}")
def delete_permission_read(permission_id: int, session: Session = Depends(get_session)):
    return delete_permission(session, permission_id)
"""
