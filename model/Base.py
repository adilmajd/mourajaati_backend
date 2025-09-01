from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

# ======================
# TABLES DE BASE
# ======================


class Ville(SQLModel, table=True):
    ville_id: Optional[int] = Field(default=None, primary_key=True)
    ville_nom: str = Field(max_length=20, unique=True)
    # Relation avec CodePostale
    code_postales: List["CodePostale"] = Relationship(back_populates="ville")
    # Relation avec Ecole
    ecoles: List["Ecole"] = Relationship(back_populates="ville")


class CodePostale(SQLModel, table=True):
    cp_id: Optional[int] = Field(default=None, primary_key=True)
    code: int = Field(unique=True)
    ville_id: int = Field(foreign_key="ville.ville_id")
    # Relation inverse
    ville: Optional[Ville] = Relationship(back_populates="code_postales")


class Niveau(SQLModel, table=True):
    niveau_id: Optional[int] = Field(default=None, primary_key=True)
    label: str = Field(max_length=20, unique=True)
    # Relation avec Ecole
    ecoles: List["Ecole"] = Relationship(back_populates="niveau")
    # Relation avec Grade
    grades: List["Grade"] = Relationship(back_populates="niveau")


class Ecole(SQLModel, table=True):
    ecole_id: Optional[int] = Field(default=None, primary_key=True)
    nom: str = Field(max_length=20)
    ville_id: int = Field(foreign_key="ville.ville_id")
    niveau_id: int = Field(foreign_key="niveau.niveau_id")
    # Relations inverses
    ville: Optional[Ville] = Relationship(back_populates="ecoles")
    niveau: Optional[Niveau] = Relationship(back_populates="ecoles")


class Grade(SQLModel, table=True):
    grade_id: Optional[int] = Field(default=None, primary_key=True)
    grade_label: str = Field(max_length=20)
    niveau_id: int = Field(foreign_key="niveau.niveau_id")
    # Relation inverse
    niveau: Optional[Niveau] = Relationship(back_populates="grades")
