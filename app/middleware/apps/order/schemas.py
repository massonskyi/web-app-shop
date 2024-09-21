from pydantic import BaseModel, Field, validator
from typing import Optional

class CreateOrderSchema(BaseModel):
    """
    Create order schema model class for pydantic validation and serialization
    """
    product_id: int = Field(..., description="Product ID")
    price: float = Field(..., description="Price of the product")
    quantity: int = Field(..., description="Quantity of the product")
    total_price: float = Field(..., description="Total price of the order")
    customer_name: str = Field(..., description="Customer's full name")
    delivery: bool = Field(False, description="Delivery flag")
    note: Optional[str] = Field(None, description="Note for the order")

    @validator('price')
    def validate_price(cls, value):
        if value < 0:
            raise ValueError('Price must be greater than or equal to 0')
        return value

    @validator('delivery')
    def validate_delivery(cls, value, values):
        if not value:
            return value

        if value and values.get('total_price', 0) < 5_000:
            raise ValueError('Delivery price must be greater than 5,000')

        return value

class UpdateOrderSchema(BaseModel):
    """
    Update order schema model class for pydantic validation and serialization
    """
    product_id: Optional[int] = Field(None, description="Product ID")
    price: Optional[float] = Field(None, description="Price of the product")
    quantity: Optional[int] = Field(None, description="Quantity of the product")
    total_price: Optional[float] = Field(None, description="Total price of the order")
    customer_name: Optional[str] = Field(None, description="Customer's full name")
    delivery: Optional[bool] = Field(None, description="Delivery flag")
    note: Optional[str] = Field(None, description="Note for the order")

    @validator('price')
    def validate_price(cls, value):
        if value is not None and value < 0:
            raise ValueError('Price must be greater than or equal to 0')
        return value

    @validator('delivery')
    def validate_delivery(cls, value, values):
        if value is None:
            return value

        if value and values.get('total_price', 0) < 5_000:
            raise ValueError('Delivery price must be greater than 5,000')

        return value