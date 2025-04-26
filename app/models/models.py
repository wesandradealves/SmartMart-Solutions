from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, func
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import enum  

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    price = Column(Float)
    brand = Column(String)
    discount_percentage = Column(Float, default=0.0) 
    products = relationship("Product", back_populates="category")
    
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    category_id = Column(Integer, ForeignKey("categories.id"))
    brand = Column(String)
    # category = relationship("Category")
    category = relationship("Category", back_populates="products")
    price_history = relationship("PriceHistory", back_populates="product")
    
class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    total_price = Column(Float)
    date = Column(DateTime)

class RoleEnum(str, enum.Enum):  
    admin = "admin"
    viewer = "viewer"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True)
    password = Column(String, nullable=False) 
    role = Column(Enum(RoleEnum), default=RoleEnum.viewer)
    created_at = Column(DateTime, default=func.now()) 

class PriceHistory(Base):
    __tablename__ = 'price_history'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    price = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)
    reason = Column(String)

    product = relationship("Product", back_populates="price_history")
