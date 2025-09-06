# main.py

from typing import Annotated,Optional
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, select
from database.base import get_session
from Routers import Users,Root, Base,Cours
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

# CORS pour Angular dev
origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(Root.router)
app.include_router(Users.router,prefix="/users", tags=["users"])
app.include_router(Base.router,prefix="/base", tags=["base"])
app.include_router(Cours.router,prefix="/cours", tags=["cours"])
