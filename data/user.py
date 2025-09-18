from typing import List
from fastapi import HTTPException,Depends,UploadFile,status
from fastapi.security import OAuth2PasswordBearer
from model.Autre import PasswordUpdate, UpdateUserRoles
from model.Base import Niveau
from model.User import Etat, Permission, Role, Role_Has_Permission, User, User_Has_Role
from sqlmodel import Session, select

from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

import os
import shutil

"""

"""

UPLOAD_DIR = "uploads/avatars"

os.makedirs(UPLOAD_DIR, exist_ok=True)

# .env 
SECRET_KEY="123456789abcdefghijklmop_Khalid_Abdelah_Badrdine_Adil"
ALGORITHM="HS256"
TOKEN_EXPIRE=60 #minute

# Pour le hash des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#shema de sécurité basé sur OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

#pour tester jwt (token)
def get_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login = payload.get("sub")
        roles = payload.get("roles",[])
        permissions = payload.get("permissions",[])
        if login is None:
            raise HTTPException(status_code=401, detail="Token invalide")
        return {
            "username":login,
            "roles":roles,
            "permissions":permissions
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")
    
def require_role(required_role: str):
    def wrapper(user=Depends(get_me)):
        if required_role not in user["roles"]:
            raise HTTPException(status_code=403, detail=f"Accès interdit : rôle {required_role} requis")
        return user
    return wrapper

def require_permission(required_permission: str):
    def wrapper(user=Depends(get_me)):
        if required_permission not in user["permissions"]:
            raise HTTPException(status_code=403, detail=f"Accès interdit : permission {required_permission} requise")
        return user
    return wrapper

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_password_hash(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password,hash_password)-> bool :
    return pwd_context.verify(plain_password,hash_password)

# ======================
# Gestion Utilisateurs
# ======================

#fonction d'authentification
def login_user(session: Session,login: str,compte_password: str):
    statement=(
            select(User)
               .where(User.login==login)
               .where(User.etat_id == 1)
               )
    user = session.exec(statement).first()
    if not user:
        return None
    if not verify_password(compte_password,user.compte_password):
        return None
    #recupérer les roles
    roles = session.exec(select(Role.role_name)
                         .join(User_Has_Role,User_Has_Role.role_id==Role.role_id)
                         .where(User_Has_Role.user_id == user.user_id)).all()

    
    #recupérer les permissions
    permissions = session.exec(
        select(Permission.permission_name)
        .join(Role_Has_Permission,Role_Has_Permission.permission_id== Permission.permission_id)
        .where(Role_Has_Permission.role_id.in_(
            select(User_Has_Role.role_id).where(User_Has_Role.user_id == user.user_id)
        ) )
    ).all()
    
    #payload (key , value )
    data_token = {
        "sub": user.login,
        "roles":roles,
        "permissions":permissions
    }
    access_token_expires = timedelta(minutes=TOKEN_EXPIRE)
    access_token = create_access_token(
        data=data_token, expires_delta=access_token_expires
    )
    return {
            "access_token": access_token,
             "token_type": "bearer",
             "user_id":user.user_public_id, # interdit
             "roles":roles,
             "permissions":permissions,
             "login":user.login
             }

def users_search(session: Session, login: str=None,nom: str=None,prenom: str=None):
    query = select(User)
    if login :
        query = query.where(User.login.like(f"%{login}%"))
    if nom :
        query = query.where(User.nom.like(f"%{nom}%"))
    if prenom :
        query = query.where(User.prenom.like(f"%{prenom}%"))
    query = query.limit(7)
    users = session.exec(query).all()
    return [
        {
            "login": u.login,
            "nom": u.nom,
            "prenom": u.prenom,
            "id": u.user_public_id
        }
        for u in users
    ]

def get_roles_permissions(session: Session,user_public_id:str):
    user = session.exec(
        select(User).where(User.user_public_id == user_public_id)
    ).first()
    roles = session.exec(
        select(Role)
        .join(User_Has_Role, User_Has_Role.role_id == Role.role_id)
        .where(User_Has_Role.user_id == user.user_id)
    ).all()
    result = []
    for role in roles:
        permissions = session.exec(
            select(Permission)
            .join(Role_Has_Permission, Role_Has_Permission.permission_id == Permission.permission_id)
            .where(Role_Has_Permission.role_id == role.role_id)
        ).all()
        result.append({
            "role_id": role.role_id,
            "role_name": role.role_name,
            "permissions": [p.permission_name for p in permissions]
        })
    return {
        "user_public_id": user.user_public_id,
        "roles": result
    }

def update_user_roles(session: Session,user_public_id: str,data: UpdateUserRoles):
        user = session.get(User, user_public_id)
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        session.exec(
            select(User_Has_Role).where(User_Has_Role.user_id == user.user_id)
            ).all()
        session.query(User_Has_Role).filter(User_Has_Role.user_id == user.user_id).delete()
        for role_id in data.role_ids:
            session.add(User_Has_Role(user_id=user.user_id, role_id=role_id))

        session.commit()
        return {"Affection effectuée."}



def get_user_etat(session: Session,user_public_id: str):
    statement = (
        select(User.user_public_id, Etat.etat_id, Etat.label)
        .join(Etat, Etat.etat_id == User.etat_id)
        .where(User.user_public_id == user_public_id)
    )
    result = session.exec(statement).first()
    if not result:
        raise HTTPException(404, "Utilisateur ou état introuvable")

    user_public_id, etat_id, label = result
    return {
        "user_public_id": user_public_id,
        "etat_id": etat_id,
        "etat_label": label}

def update_user_etat(session: Session, user_public_id: str, new_etat_id: int):
    # Récupérer l'utilisateur via user_public_id
    statement = select(User).where(User.user_public_id == user_public_id)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    # Vérifier si l'état existe
    etat = session.get(Etat, new_etat_id)
    if not etat:
        raise HTTPException(status_code=404, detail="État introuvable")

    # Mise à jour
    user.etat_id = new_etat_id
    session.add(user)
    session.commit()
    session.refresh(user)

    return {
        "message": "État mis à jour avec succès",
        "user_public_id": user.user_public_id,
        "etat_id": etat.etat_id,
        "etat_libelle": etat.label   # ou etat.etat_libelle selon ton modèle
    }

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

def upload_avatar(user_public_id: int,file: UploadFile,session: Session):

    ext = file.filename.split(".")[-1].lower()
    if ext not in {"jpg", "jpeg", "png"}:
        raise HTTPException(status_code=400, detail="Format non supporté (jpg, jpeg, png uniquement).")

    user = session.get(User, user_public_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    if user.avatar and os.path.exists(user.avatar):
        try:
            os.remove(user.avatar)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression de l'ancien avatar: {str(e)}")

    new_filename = f"user_{user_public_id}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, new_filename)

    os.makedirs(UPLOAD_DIR, exist_ok=True)  # créer le dossier si inexistant
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    user.avatar = file_path.replace("\\", "/")  # normaliser pour éviter les backslashes
    session.add(user)
    session.commit()
    session.refresh(user)

    return {"message": "Avatar mis à jour", "avatar": user.avatar}



def get_avatar(user_public_id: int,session: Session):
    statement = select(User).where(User.user_public_id == user_public_id)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur introuvable"
        )

    if not user.avatar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avatar non défini pour cet utilisateur"
        )

    return user.avatar

def update_password(user_public_id: str,passwords: PasswordUpdate,session: Session):
    user = session.exec(select(User).where(User.user_public_id == user_public_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    
    user.compte_password = get_password_hash(passwords.password1) 
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return {"message": "Mot de passe mis à jour"}


# ======================
# Gestion Rôle & Permissions
# ======================

# ---- RÔLES ----

def assign_role_to_user(session: Session, user_id: int, role_id: int):
    link = User_Has_Role(user_id=user_id, role_id=role_id)
    session.add(link)
    session.commit()
    return {"message": "Rôle assigné"}

def remove_role_from_user(session: Session, user_id: int, role_id: int):
    link = session.get(User_Has_Role, (user_id, role_id))
    if not link:
        raise HTTPException(404, "Lien non trouvé")
    session.delete(link)
    session.commit()
    return {"message": "Rôle retiré"}

def delete_role(session: Session ,role_id: int ):
    role = session.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role non trouvé")
    statement = select(Role_Has_Permission).where(Role_Has_Permission.role_id == role_id)
    results = session.exec(statement).all()
    for r in results:
        session.delete(r)
    session.flush() 
    session.delete(role)
    session.commit()
    return {"message": f"Role {role.role_name} supprimé avec toutes ses permissions"}



# ---- PERMISSIONS ----

def assign_permission_to_role(session: Session, role_id: int, permission_id: int):
    link = Role_Has_Permission(role_id=role_id, permission_id=permission_id)
    session.add(link)
    session.commit()
    return {"message": "Permission assignée"}


def delete_permission(session: Session, permission_id: int):
    stmt = select(Role_Has_Permission).where(Role_Has_Permission.permission_id == permission_id)
    relations = session.exec(stmt).all()
    for rel in relations:
        session.delete(rel)
    session.flush() 
    permission = session.get(Permission, permission_id)
    if not permission:
        raise HTTPException(404, "Permission not found")
    session.delete(permission)
    session.commit()
    return {"message": "Permission supprimée avec succès"}


def get_role_permissions(role_id: int, session: Session):
    role = session.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role non trouvé")
    all_permissions = session.exec(select(Permission)).all()
    role_permission_ids = {perm.permission_id for perm in role.permissions}
    permissions_with_status = [
        {
            "permission_id": perm.permission_id,
            "permission_name": perm.permission_name,
            "checked": perm.permission_id in role_permission_ids,
        }
        for perm in all_permissions
    ]

    return {
        "role_id": role.role_id,
        "role_name": role.role_name,
        "permissions": permissions_with_status
    }

def update_role_permissions(role_id: int,permission_ids: List[int],session: Session):
    role = session.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    permissions = session.exec(
        select(Permission).where(Permission.permission_id.in_(permission_ids))
        ).all()

    role.permissions = permissions  

    session.add(role)
    session.commit()
    session.refresh(role)
    return {"message": "Permissions mises à jour avec succès", "role": role}

def add_permission_to_role(role_id: int, permission_id: int, session: Session):
    session.add(Role_Has_Permission(role_id=role_id, permission_id=permission_id))
    session.commit()
    return {"message": "Permission associée"}

def remove_permission_from_role(role_id: int, permission_id: int, session: Session):
    stmt = select(Role_Has_Permission).where(
        Role_Has_Permission.role_id == role_id,
        Role_Has_Permission.permission_id == permission_id
    )
    link = session.exec(stmt).first()
    if link:
        session.delete(link)
        session.commit()
    return {"message": "Permission supprimée"}