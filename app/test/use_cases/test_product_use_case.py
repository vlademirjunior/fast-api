import pytest
from fastapi.exceptions import HTTPException
from app.db.models import Product as ProductModel
from app.schemas.product import Product, ProductOutput
from app.use_cases.product import ProductUseCases
from fastapi_pagination import Page


def test_add_product_use_case(db_session, categories_on_db):
    use_case = ProductUseCases(db_session)

    product = Product(
        name='Camisa Mike',
        slug='camisa-mike',
        price=22.99,
        stock=22
    )

    use_case.add_product(
        product=product, category_slug=categories_on_db[0].slug)

    product_on_db = db_session.query(ProductModel).first()

    assert product_on_db is not None
    assert product_on_db.name == product.name
    assert product_on_db.slug == product.slug
    assert product_on_db.price == product.price
    assert product_on_db.stock == product.stock
    assert product_on_db.category.name == categories_on_db[0].name

    db_session.delete(product_on_db)
    db_session.commit()


def test_add_product_user_case_invalid_category(db_session):
    use_case = ProductUseCases(db_session)

    product = Product(
        name='Camisa Mike',
        slug='camisa-mike',
        price=22.99,
        stock=22
    )

    with pytest.raises(HTTPException):
        use_case.add_product(product=product, category_slug='invalid slug')


def test_update_product(db_session, product_on_db):
    product = Product(
        name='Camisa Abibas',
        slug='camisa-abibas',
        price=22.99,
        stock=22
    )

    use_case = ProductUseCases(db_session)
    use_case.update_product(id=product_on_db.id, product=product)

    product_update_on_db = db_session.query(
        ProductModel).filter_by(id=product_on_db.id).first()

    assert product_update_on_db is not None
    assert product_update_on_db.name == product.name
    assert product_update_on_db.slug == product.slug


def test_update_product_invalid_id(db_session):
    product = Product(
        name='Camisa Abibas',
        slug='camisa-abibas',
        price=22.99,
        stock=22
    )

    use_case = ProductUseCases(db_session)
    with pytest.raises(HTTPException):
        use_case.update_product(id=0, product=product)


def test_update_product(db_session, product_on_db):
    use_case = ProductUseCases(db_session)
    use_case.delete_product(id=product_on_db.id)

    products_on_db = db_session.query(ProductModel).all()

    assert len(products_on_db) == 0


def test_update_product_non_exist(db_session):
    use_case = ProductUseCases(db_session)

    with pytest.raises(HTTPException):
        use_case.delete_product(id=0)

def test_list_products_use_case(db_session, products_on_db):
    use_case = ProductUseCases(db_session)

    page = use_case.list_products(page=1, size=2)

    assert len(page.items) == 2
    assert type(page) == Page
    assert page.total == 3
    assert page.page == 1
    assert page.size == 2
    assert page.pages == 2

    assert page.items[0].id == products_on_db[0].id
    assert page.items[1].id == products_on_db[1].id

def test_list_products_use_case_with_search(db_session, products_on_db):
    use_case = ProductUseCases(db_session)

    page = use_case.list_products(search='camisa')

    assert len(page.items) == 2
    assert type(page) == Page
    assert page.items[0].id == products_on_db[0].id
    assert page.items[1].id == products_on_db[1].id