from typing import Optional
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Float,
    Boolean,
    Table,
    Text
)

from database.connection import Base
from sqlalchemy.orm import validates
from middleware.apps import metadata

# Определение таблицы orders
order_table = Table(
    'orders',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, nullable=False, unique=True),
    Column('product_id', Integer, ForeignKey('products.id'), nullable=False),
    Column('price', Float, nullable=False),
    Column('quantity', Integer, nullable=False),
    Column('total_price', Float, nullable=False),
    Column('customer_name', String(255), nullable=False),
    Column('delivery', Boolean, nullable=False, default=False),
    Column('note', Text, nullable=True)
)

class Order(Base):
    """
    Order model class
    """
    __tablename__ = 'orders'
    id: Optional[int] = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    
    product_id: Optional[int] = Column(Integer, ForeignKey('products.id'), nullable=False) # Поле для связи с таблицей products
    
    price: Optional[float] = Column(Float, nullable=False)
    
    quantity: Optional[int] = Column(Integer, nullable=False)
    
    total_price: Optional[float] = Column(Float, nullable=False)
    
    customer_name: Optional[str] = Column(String(255), nullable=False)
    
    delivery: Optional[bool] = Column(Boolean, nullable=False, default=False) # Поле для флага доставки
    
    note: Optional[str] = Column(Text, nullable=True) # Поле для описания заказа
    
    def __init__(self, product_id: int, price: float, quantity: int, total_price: float, customer_name: str, delivery: bool, note: str): # Конструктор
        self.product_id = product_id
        self.price = price
        self.quantity = quantity
        self.total_price = total_price
        self.customer_name = customer_name
        self.delivery = delivery
        self.note = note
        
    @validates('price')
    def validate_price(self, key, value):
        if value < 0:
            raise ValueError('Price must be greater than or equal to 0')
        return value
    
    @validates('delivery')
    def validate_delivery(self, key, value):
        if not value:
            return value
        
        if value and self.total_price < 5_000:
            raise ValueError('Delivery price must be greater than 5,000')
        
        return value
