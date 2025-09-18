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


class Cycle(SQLModel, table=True):
    cycle_id: Optional[int] = Field(default=None, primary_key=True)
    label: str = Field(max_length=20, unique=True)
    # Relation avec Ecole
    ecoles: List["Ecole"] = Relationship(back_populates="cycle")
    # Relation avec Grade
    niveaux: List["Niveau"] = Relationship(back_populates="cycle")


class Ecole(SQLModel, table=True):
    ecole_id: Optional[int] = Field(default=None, primary_key=True)
    nom: str = Field(max_length=20)
    ville_id: int = Field(foreign_key="ville.ville_id")
    cycle_id: int = Field(foreign_key="cycle.cycle_id")
    # Relations inverses
    ville: Optional[Ville] = Relationship(back_populates="ecoles")
    cycle: Optional[Cycle] = Relationship(back_populates="ecoles")


class Niveau(SQLModel, table=True):
    niveau_id: Optional[int] = Field(default=None, primary_key=True)
    niveau_label: str = Field(max_length=20)
    cycle_id: int = Field(foreign_key="cycle.cycle_id")
    # Relation inverse
    cycle: Optional[Cycle] = Relationship(back_populates="niveaux")
