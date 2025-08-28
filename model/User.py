from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


# ======================
# UTILISATEURS ET ROLES
# ======================

class User(SQLModel, table=True):
    user_id: int = Field(primary_key=True)
    nom: str = Field(max_length=20)
    prenom: str = Field(max_length=20)
    mail: str = Field(max_length=20, unique=True)
    date_naissance: Optional[str]
    avatar: Optional[str] = Field(max_length=99, default=None)
    login: str = Field(max_length=20, unique=True)
    compte_password: str = Field(max_length=20)
    telephone: Optional[str] = Field(max_length=20, default=None)
    etat_id: int = Field(foreign_key="etat.etat_id")
    ecole_id: int = Field(foreign_key="ecole.ecole_id")
    ville_id: int = Field(foreign_key="ville.ville_id")
    grade_id: int = Field(foreign_key="grade.grade_id")
    
class Etat(SQLModel, table=True):
    etat_id: int = Field(primary_key=True)
    label: str = Field(max_length=20, unique=True)



class Role(SQLModel, table=True):
    role_id: int = Field(primary_key=True)
    role_name: str = Field(max_length=20)


class GroupTable(SQLModel, table=True):
    group_id: int = Field(primary_key=True)
    group_name: str = Field(max_length=20)
    role_id: int = Field(foreign_key="role.role_id")


class UserHasRole(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.user_id", primary_key=True)
    role_id: int = Field(foreign_key="role.role_id", primary_key=True)


class GroupHasUser(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.user_id", primary_key=True)
    group_id: int = Field(foreign_key="group_table.group_id", primary_key=True)


class Permission(SQLModel, table=True):
    permission_id: int = Field(primary_key=True)
    permission_name: str = Field(max_length=20)


class RoleHasPermission(SQLModel, table=True):
    role_id: int = Field(foreign_key="role.role_id", primary_key=True)
    permission_id: int = Field(foreign_key="permission.permission_id", primary_key=True)

