from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from model.Autre import UpdateUserRoles
from model.User import Etat, Permission, Role, Role_Has_Permission, User, User_Has_Role
from sqlmodel import Session, select

from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

"""

"""

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


# ---- PERMISSIONS ----


def assign_permission_to_role(session: Session, role_id: int, permission_id: int):
    link = Role_Has_Permission(role_id=role_id, permission_id=permission_id)
    session.add(link)
    session.commit()
    return {"message": "Permission assignée"}


