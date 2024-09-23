from typing import(
    Optional,
    Union
)

from fastapi import Form
from pydantic import (
    BaseModel, 
    Field, 
    EmailStr, 
    validator
)



class CreateFeedBackSchema(BaseModel):
    """
    Create FeedBack Schema class for feedback creation request 
    """


    fullname: str = Form(..., min_length=3, max_length=255)
    
    email: EmailStr = Form(..., min_length=3, max_length=50)
    
    description: str = Form(..., min_length=3, max_length=999)

    phone: str = Form(..., min_length=3, max_length=255)

    @validator('fullname')
    def validate_fullname(cls, value: str):
        name, surname, _ = value.split(' ') if value else (None, None, None)
        if not name or not surname:
            raise ValueError('Full name must be a string')
        if not name.isalpha() or not surname.isalpha():
             raise ValueError('Full name must contain only letters')
        return value
    
    @validator('email')
    def validate_email(cls, value: str):
        if not value:
            raise ValueError('Email must be a string')
        
        return value

    def validate(self) -> bool:
        """
        Validate the input data.

        Returns:
            True if the data is valid, False otherwise.
        """
        try:
            self.validate_fullname(self.fullname)
            self.validate_email(self.email)
        except ValueError:
            return False
        return True

class UpdateFeedBackSchema(BaseModel):
    """
    Update FeedBack Schema class for feedback update request
    """
    fullname: str = Form(..., min_length=3, max_length=255)
    
    email: EmailStr = Form(..., min_length=3, max_length=50)
    
    description: str = Form(..., min_length=3, max_length=999)

    phone: str = Form(..., min_length=3, max_length=255)

    @validator('fullname')
    def validate_fullname(cls, value: str):
        name, surname, _ = value.split(' ') if value else (None, None, None)
        if not name or not surname:
            raise ValueError('Full name must be a string')
        if not name.isalpha() or not surname.isalpha():
             raise ValueError('Full name must contain only letters')
        return value
    
    @validator('email')
    def validate_email(cls, value: str):
        if not value:
            raise ValueError('Email must be a string')
        
        return value

    def validate(self) -> bool:
        """
        Validate the input data.

        Returns:
            True if the data is valid, False otherwise.
        """
        try:
            self.validate_fullname(self.fullname)
            self.validate_email(self.email)
        except ValueError:
            return False
        return True

















































































































