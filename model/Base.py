from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

# ======================
# TABLES DE BASE
# ======================


class Ville(SQLModel, table=True):
    ville_id: int = Field(primary_key=True)
    ville_nom: str = Field(max_length=20, unique=True)


class CodePostale(SQLModel, table=True):
    cp_id: int = Field(primary_key=True)
    code: int = Field(unique=True)
    ville_id: int = Field(foreign_key="ville.ville_id")


class Niveau(SQLModel, table=True):
    niveau_id: int = Field(primary_key=True)
    label: str = Field(max_length=20, unique=True)


class Ecole(SQLModel, table=True):
    ecole_id: int = Field(primary_key=True)
    nom: str = Field(max_length=20)
    ville_id: int = Field(foreign_key="ville.ville_id")
    niveau_id: int = Field(foreign_key="niveau.niveau_id")


class Grade(SQLModel, table=True):
    grade_id: int = Field(primary_key=True)
    grade_label: str = Field(max_length=20)
    niveau_id: int = Field(foreign_key="niveau.niveau_id")
