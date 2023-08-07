
from decouple import config
from app.db.connection import Session
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session as SessionSql
from fastapi import Depends
from app.use_cases.user import UserUseCases

oauth_schema = OAuth2PasswordBearer(tokenUrl='/user/login')

TEST_MODE = config('TEST_MODE', default=False, cast=bool)


def get_db_session():
    try:
        session = Session()
        yield session
    finally:
        session.close()


def auth(db_session: SessionSql = Depends(get_db_session),
         token=Depends(oauth_schema)):
    if TEST_MODE:
        return
    
    user_case = UserUseCases(db_session=db_session)

    user_case.verify_token(token=token)
