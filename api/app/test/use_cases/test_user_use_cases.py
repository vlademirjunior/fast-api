import pytest
from passlib.context import CryptContext  # necessária para validação de senha
from app.schemas.user import User
from app.db.models import User as UserModel
from app.use_cases.user import UserUseCases
from fastapi.exceptions import HTTPException
from datetime import datetime, timedelta
from jose import jwt
from decouple import config

crypt_context = CryptContext(schemes=['sha256_crypt'])

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

def test_register_user(db_session):
    user = User(
        username='vlad',
        password='!2e'
    )

    use_case = UserUseCases(db_session)
    use_case.register_user(user)

    user_on_db = db_session.query(UserModel).first()

    assert user_on_db is not None
    assert user_on_db.username == user.username
    assert crypt_context.verify(user.password, user_on_db.password)

    db_session.delete(user_on_db)
    db_session.commit()


def test_register_user_username_already_exists(db_session):
    user_on_db = UserModel(
        username='vlad',
        password=crypt_context.hash('!2e')
    )

    db_session.add(user_on_db)
    db_session.commit()

    user = User(
        username='vlad',
        password=crypt_context.hash('!2e')
    )

    use_case = UserUseCases(db_session)
    with pytest.raises(HTTPException):
        use_case.register_user(user)

    db_session.delete(user_on_db)
    db_session.commit()


def test_user_login(db_session, user_on_db):
    use_case = UserUseCases(db_session)

    user = User(
        username=user_on_db.username,
        password='!2e'
    )

    token_data = use_case.user_login(user, expires_in=30)

    # 00:00
    # 00:31
    assert token_data.expires_at < datetime.utcnow() + timedelta(31)


def test_user_login_invalid_username(db_session, user_on_db):
    user_case = UserUseCases(db_session=db_session)
    user = User(
        username=user_on_db.username,
        password='invalid'
    )

    with pytest.raises(HTTPException):
        user_case.user_login(user, expires_in=30)

def test_verify_token(db_session, user_on_db):
    uc = UserUseCases(db_session=db_session)

    data = {
        'sub': user_on_db.username,
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }

    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    uc.verify_token(token=access_token)

def test_verify_token_expired(db_session, user_on_db):
    uc = UserUseCases(db_session=db_session)

    data = {
        'sub': user_on_db.username,
        'exp': datetime.utcnow() - timedelta(minutes=30)
    }

    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException):
        uc.verify_token(token=access_token)