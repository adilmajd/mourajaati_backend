from model.User import User
from sqlmodel import Session, select


def get_all_user(session: Session):
    users = session.exec(select(User)).all()
    return users