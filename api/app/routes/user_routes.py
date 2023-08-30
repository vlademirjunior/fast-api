from fastapi import APIRouter, Response, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm # para poder trabalhar com formulario de login dentro do fastapi
from app.routes.deps import get_db_session
from app.use_cases.user import UserUseCases
from app.schemas.user import User

router = APIRouter(prefix='/user', tags=['Usuários da minha loja'])


@router.post('/register', status_code=status.HTTP_201_CREATED, description='Registra novo usuário')
def add_product(user: User, db_session: Session = Depends(get_db_session)):
    use_case = UserUseCases(db_session)
    use_case.register_user(user)

    return Response(status_code=status.HTTP_201_CREATED)

@router.post('/login', status_code=status.HTTP_200_OK, description='Login do usuário')
def add_product(
    login_request_form: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_db_session)):
    use_case = UserUseCases(db_session)
    user = User(
        username=login_request_form.username,
        password=login_request_form.password
    )
    token_data = use_case.user_login(user, expires_in=60)

    return token_data