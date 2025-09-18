from fastapi import APIRouter,Depends,UploadFile
from pydantic import BaseModel
from data.CRUD import create_entity, delete_entity, get_all_entities, get_entity_by_id, update_entity
from data.user import login_user, require_permission,require_role,users_search,get_roles_permissions,update_user_roles,get_user_etat,update_user_etat,delete_role,delete_permission,get_role_permissions,add_permission_to_role,remove_permission_from_role,upload_avatar,get_avatar
from database.base import get_session
from sqlmodel import Session, select
from typing import List, Optional
from model.Autre import LoginRequest, RoleCreate, UpdateUserRoles,PermissionCreate
from model.User import Etat, Permission, Role, User
from data.user import get_password_hash,get_me
from fastapi.staticfiles import StaticFiles

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
async def list_users(session: Session = Depends(get_session),user = Depends(require_role("admin"))):
     return get_all_entities(session, User)

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int,session: Session = Depends(get_session)):
     return get_entity_by_id(session, User, user_id)

@router.get("/user/{user_public_id}/roles-permissions")
async def get_roles_permissions_r(user_public_id:str,session: Session = Depends(get_session),user = Depends(require_role("admin"))):
     return get_roles_permissions(session,user_public_id)

@router.get("/users_search/")
async def users_search_r(login: Optional[str]=None,nom: Optional[str]=None,prenom: Optional[str]=None,session: Session = Depends(get_session),user = Depends(require_role("admin"))):
     return users_search(session, login, nom,prenom)

@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updates: dict, session: Session = Depends(get_session),user: str = Depends(get_me)):
    return update_entity(session, User, user_id, updates)

@router.delete("/users/{user_id}")
def remove_user(user_id: int, session: Session = Depends(get_session)):
    return delete_entity(session, User, user_id)

@router.post("/login")
def login_user_r(request: LoginRequest, session: Session = Depends(get_session)):
    user = login_user(session,request.login,request.password)
    if not user:
        return {"message" : "erreur"}
    return {"message" : "connection ok","user":user}


@router.get("/test_me")
async def test_me(data: str = Depends(get_me)):
     return {"user login":data}

@router.put("/user/{user_id}/roles")
def update_user_roles_r(user_id: str, data: UpdateUserRoles, session: Session = Depends(get_session),user = Depends(require_role("admin"))):
  return update_user_roles(session,user_id,data)

@router.get("/user/{user_id}/etat")
def get_user_etat_r(user_id: str, session: Session = Depends(get_session)):
    return get_user_etat(session,user_id)

@router.post("/user/{user_id}/avatar")
def upload_avatar_r(user_id: str,file: UploadFile,session: Session = Depends(get_session),user = Depends(require_permission("avatar"))):
    return upload_avatar(user_id,file,session)



@router.get("/user/{user_id}/avatar")
def get_avatar_r(user_id: str,session: Session = Depends(get_session),user = Depends(require_permission("avatar"))):
    return get_avatar(user_id,session)



"""
@router.put("/{user_id}/etat/{etat_id}")
def change_user_etat_read(user_id: int, etat_id: int, session: Session = Depends(get_session)):
    return change_user_etat(session, user_id, etat_id)

@router.get("/hash/")
async def hash_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    for user in users:
        if not user.compte_password.startswith("$2b$"):
            hashed = get_password_hash(user.compte_password)
            user.compte_password = hashed
            session.add(user)
    session.commit()
"""

# ======================
# Gestion Rôle & Permissions
# ======================


# Rôles

@router.post("/roles/", response_model=Role)
def add_role(role:RoleCreate, session: Session = Depends(get_session),user = Depends(require_role("admin"))):
    db_role = Role(role_name=role.role_name)
    return create_entity(session, db_role)

@router.get("/roles/", response_model=List[Role])
async def list_roles(session: Session = Depends(get_session),user = Depends(require_role("admin"))):
     return get_all_entities(session, Role)

@router.get("/roles/{role_id}", response_model=Role)
async def get_role(role_id: int,session: Session = Depends(get_session)):
     return get_entity_by_id(session, Role, role_id)

@router.put("/roles/{role_id}", response_model=Role)
def update_role(role_id: int, updates: dict, session: Session = Depends(get_session)):
    return update_entity(session, Role, role_id, updates)

@router.delete("/roles/{role_id}")
def remove_role(role_id: int, session: Session = Depends(get_session),user = Depends(require_role("admin"))):
    return delete_role(session, role_id)


@router.get("/etats/", response_model=List[Etat])
async def list_etats(session: Session = Depends(get_session),user = Depends(require_role("admin"))):
     return get_all_entities(session, Etat)

@router.put("/user/{user_public_id}/etat/{etat_id}")
async def update_user_etat_r(user_public_id: str,etat_id: int,session: Session = Depends(get_session)):
     return update_user_etat(session,user_public_id,etat_id)

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
def add_permission(permission:PermissionCreate, session: Session = Depends(get_session),user = Depends(require_role("admin"))):
    db_permission = Permission(permission_name=permission.permission_name)
    return create_entity(session, db_permission)

@router.get("/permissions/", response_model=List[Permission])
async def list_permissions(session: Session = Depends(get_session),user = Depends(require_role("admin"))):
     return get_all_entities(session, Permission)

@router.get("/permissions/{permission_id}", response_model=Permission)
async def get_permission(permission_id: int,session: Session = Depends(get_session)):
     return get_entity_by_id(session, Permission, permission_id)

@router.put("/permissions/{permission_id}", response_model=Permission)
def update_permission(permission_id: int, updates: dict, session: Session = Depends(get_session)):
    return update_entity(session, Permission, permission_id, updates)

@router.delete("/permissions/{permission_id}")
def remove_permission(permission_id: int, session: Session = Depends(get_session),user = Depends(require_role("admin"))):
    return delete_permission(session, permission_id)

@router.get("/roles/{role_id}/permissions")
async def get_role_permissions_r(role_id: int, session: Session = Depends(get_session),user = Depends(require_role("admin"))):
     return get_role_permissions(role_id, session)

@router.post("/roles/{role_id}/permissions/{permission_id}")
def add_permission_to_role_r(role_id: int, permission_id: int, session: Session = Depends(get_session)):
    return add_permission_to_role(role_id,permission_id,session)

@router.delete("/roles/{role_id}/permissions/{permission_id}")
def remove_permission_from_role_r(role_id: int, permission_id: int, session: Session = Depends(get_session),user = Depends(require_role("admin"))):
    return remove_permission_from_role(role_id,permission_id,session)

