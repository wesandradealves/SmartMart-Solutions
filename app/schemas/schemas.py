from pydantic import BaseModel, Field, EmailStr, model_validator
from typing import Dict, Optional, Generic, TypeVar, List
from datetime import datetime
from enum import Enum  

T = TypeVar('T')

# Roles

class RoleEnum(str, Enum):
    admin = "admin"
    viewer = "viewer"
    guest = "guest"

# Response genérica

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int

# Categories

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    discount_percentage: Optional[float] = None 

    class Config:
        from_attributes = True

class CategoryCreate(CategoryBase):
    name: str 
    description: Optional[str] = None
    discount_percentage: Optional[float] = None

    @model_validator(mode='before')
    def check_name_or_description(cls, values):
        name = values.get('name')
        description = values.get('description')

        if not name and not description:
            raise ValueError('Pelo menos nome ou descrição deve ser fornecido.')
        return values

class Category(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    discount_percentage: Optional[float] = None
    total_products: Optional[int] = None

    class Config:
        from_attributes = True

# Products

class CategoryName(BaseModel):
    name: str

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None  
    price: Optional[float] = None  
    category_id: Optional[int] = None  
    brand: Optional[str] = None  

    class Config:
        from_attributes = True

    @model_validator(mode='before')
    def check_category_id(cls, values):
        category_id = values.get('category_id')

        if category_id is not None and category_id <= 0:
            raise ValueError("O campo 'category_id' deve ser um valor válido.")
        
        return values

class ProductCreate(ProductBase):
    pass

class Product(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    brand: Optional[str] = None
    category: Optional[CategoryName] = None 

    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    brand: Optional[str] = None

    class Config:
        from_attributes = True

# Sales

class SaleBase(BaseModel):
    product_id: int
    quantity: int
    total_price: float
    date: datetime

    class Config:
        from_attributes = True

class Sale(SaleBase):
    id: int

class SaleCreate(SaleBase):
    pass

class SaleWithProfit(Sale):
    profit: float

# Users

class UserBase(BaseModel):
    email: EmailStr = Field(..., example="email@domain.com")
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

class User(BaseModel):
    id: int
    email: str
    username: str
    hashed_password: str
    role: RoleEnum
    created_at: datetime

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: str

    @model_validator(mode='after')
    def check_username_or_email(self) -> 'LoginRequest':
        if not self.username and not self.email:
            raise ValueError('Você deve fornecer username ou email para login.')
        return self
    
# Price History

class PriceHistoryBase(BaseModel):
    product_id: int
    price: float
    date: datetime
    reason: Optional[str] = None

    class Config:
        from_attributes = True

class PriceHistory(PriceHistoryBase):
    id: int
