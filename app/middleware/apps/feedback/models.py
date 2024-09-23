from typing import Optional
from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    ForeignKey, 
    DateTime, 
    Boolean,
    Table,  
    TIMESTAMP, 
    Text
)

from sqlalchemy.orm import validates

from database.connection import Base
from middleware.apps import metadata

feedback_table = Table(
    'feedbacks',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, nullable=False, unique=True),    
    Column('fullname', String(255), nullable=False),
    Column('email', String(50), nullable=False, unique=True),
    Column('description', String(999), nullable=False),
    Column('phone', String(255), nullable=False)
)


class FeedBack(Base):
    """
    FeedBack class model
    """
    __tablename__ = 'feedbacks'
    id: Optional[int] = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    fullname: Optional[str] = Column(String(255), nullable=False)
    email: Optional[str] = Column(String(50), nullable=False, unique=True)
    description: Optional[str] = Column(String(999), nullable=False)
    phone: Optional[str] = Column(String(255), nullable=False)

    def __init__(self, fullname, email, description, phone) -> None:
        """
        Initialize FeedBack class model
        @param fullname: Full name
        @param email: Email
        @param description: Description of feedback 
        @return: None
        
        @raises: ValueError if fullname, email or description is empty or not string
        """
        self.fullname = fullname
        self.email = email
        self.description = description
        self.phone = phone
    
    @validates('fullname')
    def validate_fullname(self, key, value):
        name, surname, _ = value.split(' ') if value else (None, None, None)
        if not name or not surname:
            raise ValueError('Full name must be a string')
        if not name.isalpha() or not surname.isalpha():
             raise ValueError('Full name must contain only letters')
        return value
    
    @validates('email')
    def validate_email(self, key, value):
        if not value:
            raise ValueError('Email must be a string')
        
        return value
    
    @validates('description')
    def validate_description(self, key, value):
        if not value:
            raise ValueError('Description must be a string')
        
        return value
    
    def __iter__(self):
        for attr, value in self.__dict__.items():
            if not attr.startswith('_'):
                yield attr, value

    def dict(self):
        data = {}
        for attr, value in self:
            data[attr] = value
        return data