# database.py
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Text, ForeignKey, TIMESTAMP, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:1234@localhost:5432/E-commerce")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("category.id"))
    name = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    description = Column(Text)

    category = relationship("Category", back_populates="products")


class Decorator(Base):
    __tablename__ = "decorators"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    cost = Column(Numeric(10, 2), nullable=False)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False, default=0)
    created_at = Column(TIMESTAMP, server_default='NOW()')

    items = relationship("OrderItem", back_populates="order")
    decorators = relationship("OrderDecorator", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("product.id"))
    quantity = Column(SmallInteger, nullable=False, default=1)
    subtotal = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")


class OrderDecorator(Base):
    __tablename__ = "order_decorators"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    decorator_id = Column(Integer, ForeignKey("decorators.id"))

    order = relationship("Order", back_populates="decorators")
    decorator = relationship("Decorator")