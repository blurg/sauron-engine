from enum import Enum
from typing import List

from pydantic import BaseModel


class OrderStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class OrderItem(BaseModel):
    product_id: str
    quantity: int
    unit_price: float


class Order(BaseModel):
    order_id: str
    customer_id: str
    items: List[OrderItem]
    total_amount: float
    payment_method: str
    priority: str = "normal"


class OrderResponse(BaseModel):
    order_id: str
    status: OrderStatus
    processed_amount: float
    applied_discount: float
    shipping_cost: float
    final_amount: float
    results: List[dict]
