import re
from pydantic import field_validator
from app.schemas.custom_base_model import CustomBaseModel
from app.schemas.category import Category

class Product(CustomBaseModel):
    name: str
    slug: str
    price: float
    stock: int

    @field_validator('slug')
    def validate_slug(cls, value):
        if not re.match('^([a-z]|-|_)+$', value):
            raise ValueError('Invalid slug')
        return value
    
    @field_validator('price')
    def validate_price(cls, value):
        if value <= 0:
            raise ValueError('Invalid price')
        return value
    
    @field_validator('stock')
    def validate_stock(cls, value):
        if value < 0:
            raise ValueError('Invalid stock')
        return value


class ProductInput(CustomBaseModel):
    category_slug: str
    product: Product

class ProductOutput(Product):
    id: int
    category: Category