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