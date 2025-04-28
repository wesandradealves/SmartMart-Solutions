from pydantic import BaseModel, Field, EmailStr, model_validator, root_validator
from typing import Dict, Optional, Generic, TypeVar, List
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

# Categories=

class CategoryBase(BaseModel):
    name: str
    description: str
    discount_percentage: float
    class Config:
        from_attributes = True

class CategoryCreate(CategoryBase):
    name: Optional[str] = None
    description: Optional[str] = None
    discount_percentage: Optional[float] = None

    @root_validator(pre=True)
    def check_name_or_description(cls, values):
        name = values.get('name')
        description = values.get('description')

        if not name and not description:
            raise ValueError('Pelo menos nome ou descrição deve ser fornecido.')
        return values
    
class Category(CategoryBase):
    id: int
    total_products: Optional[int] = None 

# Products

class CategoryName(BaseModel):
    name: str

    class Config:
        from_attributes = True
        
@root_validator(pre=True)
def check_category_id(cls, values):
    category_id = values.get('category_id', None)

    if category_id is not None and category_id <= 0:
        raise ValueError("O campo 'category_id' deve ser um valor válido.")
    
    return values

class ProductBase(BaseModel):
    name: str = Field(..., example="Smartphone Galaxy A15")
    description: str = Field(..., example="Smartphone com tela de 6,5 polegadas")
    price: float = Field(..., gt=0, example=1299.99)
    category_id: Optional[int] = Field(None, example=2)  
    brand: str = Field(..., example="Samsung")

    class Config:
        from_attributes = True

class Product(ProductBase):
    id: int
    category: Optional[CategoryName] = None 

    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None  
    category: Optional[dict] = None 
    brand: Optional[str] = None

    @root_validator(pre=True)
    def check_category_id(cls, values):
        category_id = values.get('category_id', None)

        if category_id is not None and category_id <= 0:
            raise ValueError("O campo 'category_id' deve ser um valor válido.")
        
        return values

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
    hashed_password: str
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

