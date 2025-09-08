from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from model.User import Permission, Role, RoleHasPermission, User, UserHasRole
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


def get_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login = payload.get("sub")
        if login is None:
            raise HTTPException(status_code=401, detail="Token invalide")
        return login
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")
    
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
        return {"message":"Utilisateur introuvable"}
    if not verify_password(compte_password,user.compte_password):
        return {"message":"Mot de passe erroné"}
    access_token_expires = timedelta(minutes=TOKEN_EXPIRE)
    access_token = create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


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


