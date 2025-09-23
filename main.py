# main.py
from fastapi import FastAPI
from Routers import Users,Root, Base,Cours
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

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
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")