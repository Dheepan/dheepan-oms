from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class OrderItem(BaseModel):
    product_id: str
    quantity: int


class Order(BaseModel):
    id: str
    customer_id: str
    items: List[OrderItem]
    total_amount: float
    created_at: datetime
    updated_at: Optional[datetime] = None


class OrderCreate(BaseModel):
    customer_name: str
    product_name: str
    quantity: int
    price: float


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    product_name: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    status: Optional[str] = None


class OrderResponse(BaseModel):
    id: int
    customer_name: str
    product_name: str
    quantity: int
    price: float
    status: str

    class Config:
        orm_mode = True
