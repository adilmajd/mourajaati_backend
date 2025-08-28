
from sqlmodel import Field, Session, SQLModel, create_engine, select

DATABASE_URL = "mysql+pymysql://root:1234@localhost:3306/mourajaati"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
