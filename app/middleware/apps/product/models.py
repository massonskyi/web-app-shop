import random
from typing import Optional
from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    ForeignKey, 
    DateTime, 
    Boolean,
    MetaData, 
    Table,  
    TIMESTAMP, 
    Text,
    Float
)

from sqlalchemy.orm import validates
from database.connection import Base
from middleware.apps import metadata

product_table = Table(
    'products',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, nullable=False, unique=True),  
    Column('name', String(255), nullable=False, unique=True),
    Column('smallDescription', String(255), nullable=True),
    Column('description', String(999), nullable=True),
    Column('application', String(255), nullable=True),
    Column('structure', String(255), nullable=True),
    Column('price', Float, nullable=True),
    Column('image', String(255), nullable=True),
    Column('type', String(255), nullable=True),
    Column('status', Boolean, nullable=True),
    Column('uuid_file_store', String(255), nullable=True),
    Column('is_on_sale', Boolean, nullable=True),  # New field for sale status
    Column('sale_price', Float, nullable=True)     # New field for sale price
)


class Product(Base):
    """
    Product Model 
    """
    __tablename__ = 'products'
    
    id: Optional[int] = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    name: Optional[str] = Column(String(255), nullable=False, unique=True)
    smallDescription: Optional[str] = Column(String(255), nullable=True)
    description: Optional[str] = Column(String(999), nullable=True)
    application: Optional[str] = Column(String(255), nullable=True)
    structure: Optional[str] = Column(String(255), nullable=True)
    price: Optional[float] = Column(Float, nullable=True)
    image: Optional[str] = Column(String(255), nullable=True)
    type: Optional[str] = Column(String(255), nullable=True)
    status: Optional[bool] = Column(Boolean, nullable=True)
    uuid_file_store: Optional[str] = Column(String(255), nullable=True)
    is_on_sale: Optional[bool] = Column(Boolean, nullable=True)  # New field for sale status
    sale_price: Optional[float] = Column(Float, nullable=True)   # New field for sale price

    def __init__(self, name, smallDescription, description, application, structure, price, type, status, is_on_sale, sale_price,file):
        """
        Initialize product
        """
        self.name = name
        self.smallDescription = smallDescription
        self.description = description
        self.application = application
        self.structure = structure
        self.price = price
        self.type = type
        self.status = status
        self.is_on_sale = is_on_sale
        self.sale_price = sale_price
        # Создание папки и файлов при создании записи
        self.image=file
    def __repr__(self):
        return '<Product %r>' % self.Name
    
    @validates('price')
    def validate_price(self, key, value):
        if value < 0:
            raise ValueError('Price must be greater than or equal to 0')
        return value
    
    @validates('status')
    def validate_status(self, key, value):
        if value not in [True, False]:
            raise ValueError('Status must be True or False')
        return value
    
    @validates('is_on_sale') 
    def validate_is_on_sale(self, key, value):
        if value not in [True, False]:
            raise ValueError('is_on_sale must be True or False')
        return value

    @validates('sale_price')
    def validate_sale_price(self, key, value):
        if value is not None and value < 0:
            raise ValueError('Sale price must be greater than or equal to 0')
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
        

            
    def calculate_sale_price(self, discount_percentage: float) -> float:
        """
        Calculate the sale price based on the discount percentage.
        @params discount_percentage: The discount percentage to apply.
        @return: The calculated sale price.
        """
        if self.is_on_sale:
            return self.price * (1 - discount_percentage / 100)
        return self.price