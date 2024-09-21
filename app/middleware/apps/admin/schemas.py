import re

from typing import (
    Optional, 
    Union
)

from pydantic import (
    BaseModel, 
    Field, 
    EmailStr, 
    validator
)

from datetime import datetime


def is_valid_password(password: str) -> bool:
    """
    Check if the password meets the complexity requirements.

    Returns:
        True if the password is valid, False otherwise.
    """
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.islower() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    if not any(c in '!@#$%^&*()-_=+{}[]|;:,.<>?/' for c in password):
        return False
    return True


class AdminCreateScheme(BaseModel):
    """
    Admin create Schema for admin creation.
    """
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    surname: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Union[Optional[EmailStr], str] = Field(..., min_length=2, max_length=50)
    phone: Optional[str] = Field(None, min_length=2, max_length=50)
    password: Optional[str] = Field(None, min_length=8, max_length=255)
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    
    @validator('name', 'surname')
    def check_alpha_fields(cls, value: str) -> str:
        if not value.isalpha():
            raise ValueError(f"{value} must contain only alphabetic characters.")
        return value

    @validator('phone')
    def validate_phone(cls, value: str) -> str:
        phone_pattern = re.compile(r'^\+?[1-9]\d{1,14}$')
        if not phone_pattern.match(value):
            raise ValueError("Invalid phone number format.")
        return value

    @validator('password')
    def validate_password(cls, value: str) -> str:
        if not is_valid_password(value):
            raise ValueError("Password does not meet complexity requirements.")
        return value

    def validate(self) -> bool:
        """
        Validate the input data.

        Returns:
            True if the data is valid, False otherwise.
        """
        try:
            self.check_alpha_fields(self.name)
            self.check_alpha_fields(self.surname)
            self.validate_phone(self.phone)
            self.validate_password(self.password)
        except ValueError:
            return False
        return True
    
class AdminUpdateScheme(BaseModel):
    """
    Admin update Schema for admin update.
    """
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    surname: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[Union[EmailStr, str]] = Field(None, min_length=2, max_length=50)
    phone: Optional[str] = Field(None, min_length=2, max_length=50)
    password: Optional[str] = Field(None, min_length=8, max_length=255)
    username: Optional[str] = Field(None, min_length=3, max_length=50)

    @validator('name', 'surname')
    def check_alpha_fields(cls, value: str) -> str:
        if not value.isalpha():
            raise ValueError(f"{value} must contain only alphabetic characters.")
        return value

    @validator('phone')
    def validate_phone(cls, value: str) -> str:
        phone_pattern = re.compile(r'^\+?[1-9]\d{1,14}$')
        if not phone_pattern.match(value):
            raise ValueError("Invalid phone number format.")
        return value

    @validator('password')
    def validate_password(cls, value: str) -> str:
        if not is_valid_password(value):
            raise ValueError("Password does not meet complexity requirements.")
        return value

    def validate(self) -> bool:
        """
        Validate the input data.

        Returns:
            True if the data is valid, False otherwise.
        """
        try:
            if self.name:
                self.check_alpha_fields(self.name)
            if self.surname:
                self.check_alpha_fields(self.surname)
            if self.phone:
                self.validate_phone(self.phone)
            if self.password:
                self.validate_password(self.password)
        except ValueError:
            return False
        return True
    
    
class AdminSignInScheme(BaseModel):
    """
    Admin sign in Schema for admin sign in.
    """
    password: Optional[str] = Field(None, min_length=8, max_length=255)
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    
    
    @validator('password')
    def validate_password(cls, value: str) -> str:
        if not is_valid_password(value):
            raise ValueError("Password does not meet complexity requirements.")
        return value

    def validate(self) -> bool:
        """
        Validate the input data.

        Returns:
            True if the data is valid, False otherwise.
        """
        try:
            if self.password:
                self.validate_password(self.password)
        except ValueError:
            return False
        return True

# Модель токена
class Token(BaseModel):
    """
    Model token Schema.
    """
    access_token: str
    token_type: str

# Модель данных токена
class TokenData(BaseModel):
    """
    Token data Schema.
    """
    username: Optional[str] = None