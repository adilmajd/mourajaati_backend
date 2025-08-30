from fastapi import APIRouter,Depends
from data.user import delete_user, get_all_user, get_user_by_mail, get_user_by_nom, update_user
from database.base import get_session
from sqlmodel import Session, select



router = APIRouter()

@router.get("/")
async def read_root():
    return {"message": "Users"}

@router.get("/all/")
async def get_all_user_read(session: Session = Depends(get_session)):
     return get_all_user(session)

@router.get("/nom/{nom}")
async def get_user_by_nom_read(nom: str,session: Session = Depends(get_session)):
     return get_user_by_nom(session,nom)

@router.get("/mail/{mail}")
async def get_user_by_mail_read(mail: str,session: Session = Depends(get_session)):
     return get_user_by_mail(session,mail)

@router.put("/{user_id}")
def modify_user(user_id: int, updates: dict, session: Session = Depends(get_session)):
    return update_user(session, user_id, updates)

@router.delete("/{user_id}")
def remove_user(user_id: int, session: Session = Depends(get_session)):
    return delete_user(session, user_id)


