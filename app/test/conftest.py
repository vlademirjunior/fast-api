# fixtures = recursos externos utilizados como injecao de dependencia nos nossos testes
import pytest
from app.db.connection import Session
from app.db.models import Category as CategoryModels
from app.db.models import Product as ProductModel  # sem s é o certo
from app.db.models import User as UserModel
from passlib.context import CryptContext

crypt_context = CryptContext(schemes=['sha256_crypt'])


@pytest.fixture()
def db_session():
    try:
        session = Session()
        yield session  # quando terminar de executar a funcao de teste atual, usando o yield ele fecha a sessao automaticamente
    finally:
        session.close()


@pytest.fixture()
def categories_on_db(db_session):
    categories = [
        CategoryModels(
            name='Roupa',
            slug='roupa'
        ),
        CategoryModels(
            name='Tênis',
            slug='tenis'
        ),
        CategoryModels(
            name='Decoração',
            slug='decoracao'
        ),
    ]

    for category in categories:
        db_session.add(category)

    db_session.commit()

    for category in categories:
        db_session.refresh(category)

    yield categories

    for category in categories:
        db_session.delete(category)

    db_session.commit()


@pytest.fixture()
def product_on_db(db_session):
    category = CategoryModels(
        name='Roupa',
        slug='roupa'
    )

    db_session.add(category)

    db_session.commit()
    db_session.refresh(category)

    product = ProductModel(
        category_id=category.id,
        name='Camisa mike',
        slug='camisa-mike',
        price=29.99,
        stock=100
    )

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    yield product

    db_session.delete(product)
    db_session.delete(category)
    db_session.commit()


@pytest.fixture()
def products_on_db(db_session):
    category = CategoryModels(
        name='Roupa',
        slug='roupa'
    )

    db_session.add(category)

    db_session.commit()
    db_session.refresh(category)

    products = [
        ProductModel(
            category_id=category.id,
            name='Camisa mike',
            slug='camisa-mike',
            price=26549.96459,
            stock=342454356
        ),
        ProductModel(
            category_id=category.id,
            name='Camisa abidas',
            slug='camisa-abidas',
            price=29757.997657,
            stock=4324
        ),
        ProductModel(
            category_id=category.id,
            name='Short osklei',
            slug='short-osklei',
            price=2987.99,
            stock=423432
        )
    ]

    for product in products:
        db_session.add(product)

    db_session.commit()

    for product in products:
        db_session.refresh(product)

    yield products

    for product in products:
        db_session.delete(product)

    db_session.delete(category)
    db_session.commit()



@pytest.fixture()
def user_on_db(db_session):
    user = UserModel(
        username='vlad',
        password=crypt_context.hash('!2e')
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    yield user
    db_session.delete(user)
    db_session.commit()