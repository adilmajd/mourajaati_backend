# main.py

from typing import Annotated,Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, select

from data.user import get_all_user
from database.base import get_session
from Routers import Users,Root, Base,Cours


app = FastAPI()

app.include_router(Root.router)
app.include_router(Users.router,prefix="/users", tags=["users"])
app.include_router(Base.router,prefix="/base", tags=["base"])
app.include_router(Cours.router,prefix="/cours", tags=["cours"])
