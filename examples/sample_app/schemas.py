from decimal import Decimal
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
    unit_price: Decimal


class Order(BaseModel):
    order_id: str
    customer_id: str
    items: List[OrderItem]
    total_amount: Decimal
    payment_method: str
    priority: str = "normal"


class OrderResponse(BaseModel):
    order_id: str
    status: OrderStatus
    processed_amount: Decimal
    applied_discount: Decimal
    shipping_cost: Decimal
    final_amount: Decimal
    results: List[dict]
