import datetime
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
# Table admin for alembic migrations
admin_table = Table(
    'admins',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, nullable=False, unique=True),    
    Column('name', String(50), nullable=False),
    Column('surname', String(50), nullable=False),
    Column('email', String(50), nullable=False, unique=True),
    Column('phone', String(50), nullable=False),
    Column('username', String(50), nullable=False, unique=True),
    Column('password', String(255), nullable=False),
    Column('created_at', DateTime, default=datetime.datetime.utcnow, nullable=False),
)


class Admin(Base):
    """
    Admin model for database 
    """
    __tablename__ = 'admins'
    id: Optional[int] = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    name: Optional[str] = Column(String(50), index=True, nullable=False)
    surname: Optional[str] = Column(String(50), nullable=False)
    email: Optional[str] = Column(String(50), unique=True, index=True)
    phone: Optional[str] = Column(String(50), nullable=True)
    username: Optional[str] = Column(String(50), unique=True, index=True)
    password: Optional[str] = Column(String(255))
    created_at: Optional[DateTime] = Column(DateTime, default=datetime.datetime.utcnow)

    @validates('name', 'surname')
    def validate_names(self, key, value):
        if not isinstance(value, str):
            raise ValueError(f'{key.capitalize()} must be a string')
        if not value.isalpha():
            raise ValueError(f'{key.capitalize()} must only contain letters')
        return value

    @validates('username')
    def validate_username(self, key, value):
        if not isinstance(value, str):
            raise ValueError('Username must be a string')
        if len(value) < 3:
            raise ValueError('Username must be at least 3 characters long')
        if ' ' in value:
            raise ValueError('Username cannot contain spaces')
        return value

    def __iter__(self):
        for attr, value in self.__dict__.items():
            if not attr.startswith('_'):
                yield attr, value

    def dict(self):
        data = {}
        for attr, value in self:
            if isinstance(value, datetime.datetime):
                data[attr] = value.isoformat()  # Convert datetime to ISO format string
            else:
                data[attr] = value
        return data