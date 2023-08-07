from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.base import Base, TrackTimeMixin, SoftDeleteMixin


class Category(Base):
    __tablename__ = 'categories'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String, nullable=False)
    slug = Column('slug', String, nullable=False, unique=True)
    
    products = relationship('Product', back_populates='category') # category.products -> traz todos os produtos naquela category é obrigado fazer as duas vias da relationship


class Product(Base, TrackTimeMixin, SoftDeleteMixin):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(ForeignKey('categories.id'), nullable=False)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)

    category = relationship('Category', back_populates='products') # product.category.name -> traz a name category

class User(Base, TrackTimeMixin, SoftDeleteMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)