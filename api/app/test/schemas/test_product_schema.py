import pytest
from app.schemas.product import Product, ProductInput, ProductOutput
from app.schemas.category import CategoryOutput


def test_product_schema():
    product = Product(
        name='Camisa mike',
        slug='camisa-mike',
        price=29.99,
        stock=100
    )

    assert product.model_dump() == {
        'name': 'Camisa mike',
        'slug': 'camisa-mike',
        'price': 29.99,
        'stock': 100
    }


def test_product_schema_invalid_slug():
    with pytest.raises(ValueError):
        Product(
            name='Camisa mike',
            slug='Camisa-mike',
            price=29.99,
            stock=100
        )

    with pytest.raises(ValueError):
        Product(
            name='Camisa mike',
            slug='çamisa-mike',
            price=29.99,
            stock=100
        )

    with pytest.raises(ValueError):
        Product(
            name='Camisa mike',
            slug='Camisa-mike',
            price=0,
            stock=100
        )

    with pytest.raises(ValueError):
        Product(
            name='Camisa mike',
            slug='Camisa-mike',
            price=10,
            stock=-100
        )


def test_product_input_schema():
    product = Product(
        name='Camisa Mike',
        slug='camisa-mike',
        price=29.99,
        stock=100
    )

    product_input = ProductInput(
        category_slug='roupa',
        product=product
    )

    assert product_input.model_dump() == {
        "category_slug": "roupa",
        "product": {
            "name": "Camisa Mike",
            "slug": "camisa-mike",
            "price": 29.99,
            "stock": 100
        }
    }


def test_product_output_schema():
    category = CategoryOutput(id=1, name='Roupa', slug='roupa')
    product_output = ProductOutput(
        id=1,
        name='Camisa Mike',
        slug='camisa-mike',
        price=29.99,
        stock=100,
        category=category
    )

    assert product_output.model_dump() == {
        "id": 1,
        "name": "Camisa Mike",
        "slug": "camisa-mike",
        "price": 29.99,
        "stock": 100,
        "category": category.model_dump()
    }
