from fastapi.testclient import TestClient
from fastapi import status
from app.db.models import Product as ProductModel
from app.main import app

client = TestClient(app)
headers = {"Authorization": "Bearer token"}
client.headers = headers

def test_add_product_route(db_session, categories_on_db):
    body = {
        "category_slug": categories_on_db[0].slug,
        "product": {
            "name": "Camisa Mike",
            "slug": "camisa-mike",
            "price": 23.99,
            "stock": 23
        }
    }

    response = client.post('/product/add', json=body)

    assert response.status_code == status.HTTP_201_CREATED

    products_on_db = db_session.query(ProductModel).all()

    assert len(products_on_db) == 1

    db_session.delete(products_on_db[0])
    db_session.commit()


def test_add_product_route_invalid_category_slug(db_session):
    body = {
        "category_slug": 'invalid category',
        "product": {
            "name": "Camisa Mike",
            "slug": "camisa-mike",
            "price": 23.99,
            "stock": 23
        }
    }

    response = client.post('/product/add', json=body)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    products_on_db = db_session.query(ProductModel).all()

    assert len(products_on_db) == 0


def test_update_product_route(db_session, product_on_db):
    body = {
        "name": "Camisa osklei",
        "slug": "camisa-osklei",
        "price": 213.99,
        "stock": 232
    }

    response = client.put(f'/product/update/{product_on_db.id}', json=body)

    assert response.status_code == status.HTTP_200_OK

    db_session.refresh(product_on_db)
    assert product_on_db.name == 'Camisa osklei'
    assert product_on_db.slug == 'camisa-osklei'
    assert product_on_db.price == 213.99
    assert product_on_db.stock == 232


def test_update_product_route_invalid_id():
    body = {
        "name": "Camisa osklei",
        "slug": "camisa-osklei",
        "price": 213.99,
        "stock": 232
    }

    response = client.put('/product/update/0', json=body)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_product_route(db_session, product_on_db):
    response = client.delete(f'/product/delete/{product_on_db.id}')

    assert response.status_code == status.HTTP_204_NO_CONTENT

    products_on_db = db_session.query(ProductModel).all()

    assert len(products_on_db) == 0


def test_delete_product_route_invalid_id():
    response = client.delete('/product/delete/0')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_list_products_route(products_on_db):
    response = client.get('/product/list')

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert len(data) == 3
    assert data[0] == {'name': products_on_db[0].name, 'slug': products_on_db[0].slug, 'price': products_on_db[0].price, 'stock': products_on_db[0].stock,
                       'id': products_on_db[0].id, 'category': {'name': products_on_db[0].category.name, 'slug': products_on_db[0].category.slug}}

def test_list_products_route_with_search(products_on_db):
    response = client.get('/product/list?search=cami')

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert len(data) == 2
    assert data[0] == {'name': products_on_db[0].name, 'slug': products_on_db[0].slug, 'price': products_on_db[0].price, 'stock': products_on_db[0].stock,
                       'id': products_on_db[0].id, 'category': {'name': products_on_db[0].category.name, 'slug': products_on_db[0].category.slug}}
