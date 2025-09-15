from pydantic import BaseModel
from typing import List, Optional


class LoginRequest(BaseModel):
    login: str
    password: str

class UpdateUserRoles(BaseModel):
    role_ids: List[int] 

class RoleCreate(BaseModel):
    role_name: str