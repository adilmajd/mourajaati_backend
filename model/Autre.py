from pydantic import BaseModel,validator
from typing import List, Optional


class LoginRequest(BaseModel):
    login: str
    password: str

class UpdateUserRoles(BaseModel):
    role_ids: List[int] 

class RoleCreate(BaseModel):
    role_name: str

class PermissionCreate(BaseModel):
    permission_name: str

class PasswordUpdate(BaseModel):
    password1: str
    password2: str

    @validator("password2")
    def passwords_match(cls, v, values):
        if "password1" in values and v != values["password1"]:
            raise ValueError("Les mots de passe ne correspondent pas")
        return v
    

class NiveauRead(BaseModel):
    niveau_id: int
    niveau_label: str
    order: int
    cycle_id: int

    class Config:
        from_attributes = True

class NiveauOut(BaseModel):
    niveau_id: int
    niveau_label: str
    order: int
    cycle_id: int

    class Config:
        orm_mode = True  


class UpdateUserNiveau(BaseModel):
    niveau_id: int

class UserDetailResponse(BaseModel):
    nom: str
    prenom: str
    mail: str
    date_naissance: Optional[str]
    avatar: Optional[str]
    login: str
    telephone: Optional[str]
    ecole_nom: Optional[str]
    niveau_label: Optional[str]
    cycle_label: Optional[str]

    class Config:
        from_attributes = True   # (remplace orm_mode en Pydantic v2)

class TypeCreate(BaseModel):
    type_cours_nom: str


###################################
class NiveauRead(BaseModel):
    niveau_id: int
    niveau_label: str
    class Config:
        from_attributes = True

class TypeCoursRead(BaseModel):
    type_cours_id: int
    type_cours_nom: str
    class Config:
        from_attributes = True

class CoursRead(BaseModel):
    cours_id: int
    cours_titre: str
    niveau: NiveauRead
    type_cours: TypeCoursRead
    class Config:
        from_attributes = True

class CoursReadUser(BaseModel):
    cours_id: int
    cours_titre: str
    type_cours: TypeCoursRead
    class Config:
        from_attributes = True

class CoursUpdate(BaseModel):
    niveau_id: int
    type_cours_id: int
    class Config:
        from_attributes = True

class CoursCreate(BaseModel):
    cours_titre: str
    niveau_id: int
    type_cours_id: int
    user_public_id: str 


class CoursCreateAdd(BaseModel):
    user_id: int 
    cours_titre: str
    niveau_id: int
    type_cours_id: int
    class Config:
        from_attributes = True

class CoursContenuUpdate(BaseModel):
    cours_id: int
    contenu: str
    class Config:
        from_attributes = True
