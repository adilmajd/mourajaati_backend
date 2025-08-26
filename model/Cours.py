from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
# ======================
# COURS ET CONTENU
# ======================

class Cours(SQLModel, table=True):
    cours_id: int = Field(primary_key=True)
    cours_titre: str = Field(max_length=99)
    contenu: Optional[str]
    video: Optional[str] = Field(max_length=20, default=None)
    audio: Optional[str] = Field(max_length=20, default=None)
    url: Optional[str] = Field(max_length=20, default=None)
    grade_id: int = Field(foreign_key="grade.grade_id")
    user_id: int = Field(foreign_key="user.user_id")


class Exercice(SQLModel, table=True):
    exercice_id: int = Field(primary_key=True)
    exercice_contenu: Optional[str]
    corrige: Optional[str]
    cours_id: int = Field(foreign_key="cours.cours_id")


class Post(SQLModel, table=True):
    post_id: int = Field(primary_key=True)
    post_title: str = Field(max_length=99)
    post_contenu: Optional[str] = Field(max_length=999, default=None)
    post_date_insert: Optional[str]
    post_date_update: Optional[str]
    cours_id: int = Field(foreign_key="cours.cours_id")
    user_id: int = Field(foreign_key="user.user_id")


class Comment(SQLModel, table=True):
    comment_id: int = Field(primary_key=True)
    comment_post: Optional[str] = Field(max_length=999, default=None)
    comment_date_insert: Optional[str]
    comment_date_update: Optional[str]
    post_id: int = Field(foreign_key="post.post_id")
    user_id: int = Field(foreign_key="user.user_id")


class Examen(SQLModel, table=True):
    examen_id: int = Field(primary_key=True)
    examen_contenu: Optional[str]
    examen_corrige: Optional[str]
    grade_id: int = Field(foreign_key="grade.grade_id")


class UserExamen(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.user_id", primary_key=True)
    examen_id: int = Field(foreign_key="examen.examen_id", primary_key=True)
    contenu: Optional[str]
    contenu_path: Optional[str] = Field(max_length=20, default=None)
    note: Optional[float]


class UserExercice(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.user_id", primary_key=True)
    exercice_id: int = Field(foreign_key="exercice.exercice_id", primary_key=True)
    contenu: Optional[str]
    contenu_path: Optional[str] = Field(max_length=20, default=None)
    note: Optional[float]
