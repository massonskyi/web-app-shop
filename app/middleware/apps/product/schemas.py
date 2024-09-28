from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Field, field_validator
from typing import Optional

class CreateProductSchema(BaseModel):
    """
    Create product schema model class for pydantic validation and serialization
    """
    name: Optional[str] = Form(..., description="")  
    smallDescription: Optional[str] = Form(..., description="")
    description: Optional[str] = Form(..., description="")
    application: Optional[str] = Form(..., description="")
    structure: Optional[str] = Form(..., description="")
    price: Optional[float] = Form(..., description="")
    type: Optional[str] = Form(..., description="")
    status: Optional[bool] = Form(..., description="")
    is_on_sale: Optional[bool] = Form(..., description="")
    sale_price: Optional[float] = Form(..., description="")
    file: Optional[UploadFile] = File(..., description="", media_type="image/*")
   
    def __repr__(self):
        return '<Product %r>' % self.name

    @field_validator('price')
    def validate_price(cls, value: float):
        if value < 0:
            raise ValueError('Price must be greater than or equal to 0')
        return value

    @field_validator('status')
    def validate_status(cls, value: bool):
        if value not in [True, False]:
            raise ValueError('Status must be True or False')
        return value

    @field_validator('is_on_sale')
    def validate_is_on_sale(cls, value: bool):
        if value not in [True, False]:
            raise ValueError('is_on_sale must be True or False')
        return value

    @field_validator('sale_price')
    def validate_sale_price(cls, value: float):
        if value is not None and value < 0:
            raise ValueError('Sale price must be greater than or equal to 0')
        return value

    def validate(self) -> bool:
        """
        Validate the input data.

        Returns:
            True if the data is valid, False otherwise.
        """
        try:
            self.validate_price(self.price)
            self.validate_status(self.status)
            self.validate_is_on_sale(self.is_on_sale)
            self.validate_sale_price(self.sale_price)
        except ValueError:
            return False
        return True

class UpdateProductSchema(CreateProductSchema):
    """
    Update product schema model class for pydantic validation and serialization
    """

    name: Optional[str] = Form(None, description="Name of the product", min_length=1, max_length=255)
    smallDescription: Optional[str] = Form(None, description="Small description of the product", min_length=1, max_length=255)
    description: Optional[str] = Form(None, description="Description of the product", min_length=1, max_length=999)
    application: Optional[str] = Form(None, description="Application of the product", min_length=1, max_length=255)
    structure: Optional[str] = Form(None, description="Structure of the product", min_length=1, max_length=255)
    price: Optional[float] = Form(None, description="Price of the product")
    file: Optional[UploadFile]  = File(...,description="",media_type="image/*")
    type: Optional[str] = Form(None, description="Type of the product", min_length=1, max_length=255)
    status: Optional[bool] = Form(None, description="Status of the product")
    is_on_sale: Optional[bool] = Form(None, description="Is the product on sale")
    sale_price: Optional[float] = Form(None, description="Sale price of the product")

    def __repr__(self):
        return '<Product %r>' % self.name

    @field_validator('price')
    def validate_price(cls, value: float):
        if value < 0:
            raise ValueError('Price must be greater than or equal to 0')
        return value

    @field_validator('status')
    def validate_status(cls, value: bool):
        if value not in [True, False]:
            raise ValueError('Status must be True or False')
        return value

    @field_validator('is_on_sale')
    def validate_is_on_sale(cls, value: bool):
        if value not in [True, False]:
            raise ValueError('is_on_sale must be True or False')
        return value

    @field_validator('sale_price')
    def validate_sale_price(cls, value: float):
        if value is not None and value < 0:
            raise ValueError('Sale price must be greater than or equal to 0')
        return value

    def validate(self) -> bool:
        """
        Validate the input data.

        Returns:
            True if the data is valid, False otherwise.
        """
        try:
            self.validate_price(self.price)
            self.validate_status(self.status)
            self.validate_is_on_sale(self.is_on_sale)
            self.validate_sale_price(self.sale_price)
        except ValueError:
            return False
        return True
