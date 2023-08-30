from typing import List
from fastapi import APIRouter, Response, Depends, status, Query
from sqlalchemy.orm import Session
from app.routes.deps import get_db_session, auth
from app.use_cases.product import ProductUseCases
from app.schemas.product import Product, ProductInput, ProductOutput
from fastapi_pagination import Page

router = APIRouter(prefix='/product', tags=['Produtos da minha loja'], dependencies=[Depends(auth)])


@router.post('/add', status_code=status.HTTP_201_CREATED, description='Adiciona novo produto')
def add_product(product_input: ProductInput, db_session: Session = Depends(get_db_session)):
    use_case = ProductUseCases(db_session)
    use_case.add_product(product=product_input.product,
                         category_slug=product_input.category_slug)

    return Response(status_code=status.HTTP_201_CREATED)


@router.put('/update/{id}')
def add_product(id: int, product: Product, db_session: Session = Depends(get_db_session)):
    use_case = ProductUseCases(db_session)
    use_case.update_product(id, product)

    return Response(status_code=status.HTTP_200_OK)


@router.delete('/delete/{id}')
def delete_product(id: int, db_session: Session = Depends(get_db_session)):
    use_case = ProductUseCases(db_session)
    use_case.delete_product(id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/list', response_model=Page[ProductOutput], description="Lista os produtos")
def list_products(
    page: int = Query(1, ge=1, description='Numero da pagina'),
    size: int = Query(10, ge=1, le=50, description='Tamanho da pagina'),
    search: str = '',
    db_session: Session = Depends(get_db_session)):
    use_case = ProductUseCases(db_session)
    return use_case.list_products(page=page, size=size, search=search)