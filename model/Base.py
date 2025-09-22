from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

# ======================
# TABLES DE BASE
# ======================


class Cycle(SQLModel, table=True):
    cycle_id: Optional[int] = Field(default=None, primary_key=True)
    label: str = Field(max_length=20, unique=True)
    order: int = Field()
    # Relation avec Grade
    niveaux: List["Niveau"] = Relationship(back_populates="cycle")


class Niveau(SQLModel, table=True):
    niveau_id: Optional[int] = Field(default=None, primary_key=True)
    niveau_label: str = Field(max_length=20)
    order: int = Field()
    cycle_id: int = Field(foreign_key="cycle.cycle_id")
    # Relation inverse
    cycle: Optional[Cycle] = Relationship(back_populates="niveaux")
