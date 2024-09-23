from fastapi import Form
from pydantic import BaseModel, Field, validator
from typing import Optional

class CreateOrderSchema(BaseModel):
    """
    Create order schema model class for pydantic validation and serialization
    """
    product_id: int = Form(..., description="Product ID")
    price: float = Form(..., description="Price of the product")
    quantity: int = Form(..., description="Quantity of the product")
    total_price: float = Form(..., description="Total price of the order")
    customer_name: str = Form(..., description="Customer's full name")
    delivery: bool = Form(False, description="Delivery flag")
    note: Optional[str] = Form(None, description="Note for the order")



class UpdateOrderSchema(BaseModel):
    """
    Update order schema model class for pydantic validation and serialization
    """
    product_id: Optional[int] = Form(None, description="Product ID")
    price: Optional[float] = Form(None, description="Price of the product")
    quantity: Optional[int] = Form(None, description="Quantity of the product")
    total_price: Optional[float] = Form(None, description="Total price of the order")
    customer_name: Optional[str] = Form(None, description="Customer's full name")
    delivery: Optional[bool] = Form(None, description="Delivery flag")
    note: Optional[str] = Form(None, description="Note for the order")
