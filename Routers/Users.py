from fastapi import APIRouter,Depends
from data.user import get_all_user
from database.base import get_session
from sqlmodel import Session, select



router = APIRouter()

@router.get("/")
async def read_root():
    return {"message": "Users"}

@router.get("/all/")
async def read_root(session: Session = Depends(get_session)):
     return get_all_user(session)

@router.get("/add/")
async def read_root():
    return {"message": " addUsers"}

