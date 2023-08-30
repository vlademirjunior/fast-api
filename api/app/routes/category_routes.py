from typing import List
from fastapi import APIRouter, Depends, Response, status, Query
from sqlalchemy.orm import Session
from app.schemas.category import Category, CategoryOutput
from app.routes.deps import get_db_session, auth
from app.use_cases.category import CategoryUseCases
from fastapi_pagination import Page, add_pagination, Params


router = APIRouter(prefix='/category',
                   tags=['Categorias do Produto'], dependencies=[Depends(auth)])


@router.post('/add', status_code=status.HTTP_201_CREATED, description='Adiciona nova categoria')
def add_category(
    category: Category,
    db_session: Session = Depends(get_db_session)
):
    use_case = CategoryUseCases(db_session)
    use_case.add_category(category)
    return Response(status_code=status.HTTP_201_CREATED)


@router.get('/list', response_model=Page[CategoryOutput], description="Lista as categorias")
def list_category(
        page: int = Query(1, ge=1, description='Page Number'),
        size: int = Query(10, ge=1, le=50, description='Size of page'),
        db_session: Session = Depends(get_db_session)):
    use_case = CategoryUseCases(db_session)
    return use_case.list_categories(page=page, size=size)


@router.delete('/delete/{id}')
def delete_category(
        id: int,
        db_session: Session = Depends(get_db_session)):
    use_case = CategoryUseCases(db_session)
    use_case.delete_category(id=id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
