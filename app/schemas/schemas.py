from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    description: str
    price: float
    brand: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: str = Field(..., example="Smartphone Galaxy A15")
    description: str = Field(..., example="Smartphone com tela de 6,5 polegadas")
    price: float = Field(..., gt=0, example=1299.99)
    category_id: int = Field(..., example=2)
    brand: str = Field(..., example="Samsung")

class Product(ProductBase):
    id: int
    class Config:
        orm_mode = True

class ProductCreate(ProductBase):
    pass

class SaleBase(BaseModel):
    product_id: int
    quantity: int
    total_price: float
    date: datetime 

class Sale(SaleBase):
    id: int
    class Config:
        orm_mode = True

class SaleCreate(SaleBase):
    pass

class SaleWithProfit(Sale):
    profit: float