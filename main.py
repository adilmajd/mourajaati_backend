# main.py

from typing import Annotated,Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, select

from data.user import get_all_user
from database.base import get_session
from model.Base import Ville
from model.User import User
from Routers import Users,Root


app = FastAPI()

app.include_router(Root.router)
app.include_router(Users.router,prefix="/users", tags=["users"])
