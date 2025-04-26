from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Generic, TypeVar, List
from datetime import datetime
from enum import Enum  

T = TypeVar('T')

class RoleEnum(str, Enum):
    admin = "admin"
    viewer = "viewer"
    guest = "guest"

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int

# Categories

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
        from_attributes = True 

# Products

class ProductBase(BaseModel):
    name: str = Field(..., example="Smartphone Galaxy A15")
    description: str = Field(..., example="Smartphone com tela de 6,5 polegadas")
    price: float = Field(..., gt=0, example=1299.99)
    category_id: int = Field(..., example=2)
    brand: str = Field(..., example="Samsung")

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True

class ProductCreate(ProductBase):
    pass

# Sales

class SaleBase(BaseModel):
    product_id: int
    quantity: int
    total_price: float
    date: datetime

class Sale(SaleBase):
    id: int

    class Config:
        from_attributes = True

class SaleCreate(SaleBase):
    pass

class SaleWithProfit(Sale):
    profit: float

# Users

class UserBase(BaseModel):
    email: str = Field(..., example="email@domain.com")
    username: str = Field(..., example="admin")
    role: RoleEnum = RoleEnum.viewer
    created_at: datetime = Field(default_factory=datetime.now)

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None

class User(UserBase):
    id: int

    class Config:
        from_attributes = True
        
class UserWithPassword(UserBase):
    hashed_password: str