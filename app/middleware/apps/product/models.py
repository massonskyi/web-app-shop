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

    def __init__(self, name, smallDescription, description, application, structure, price, image, type, status):
        """
        Initialize product
        """
        self.name = name
        self.smallDescription = smallDescription
        self.description = description
        self.application = application
        self.structure = structure
        self.price = price
        self.image = image
        self.type = type
        self.status = status
    
        # Создание папки и файлов при создании записи
        self.create_product_files()
        
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
        

    def create_product_files(self):
        """
        Create product files in storage folder
        """
        import os
        import json
        import uuid
        self.uuid_file_store = str(uuid.uuid4())[:8] # Создание случайного UUID для файла
        # Создание папки для продукта
        product_folder = os.path.join('storage', f'{self.name}_{self.uuid_file_store}')
        os.makedirs(product_folder, exist_ok=True)

        # Создание JSON файла
        product_info = {
            'id': self.id,
            'name': self.name,
            'smallDescription': self.smallDescription,
            'description': self.description,
            'application': self.application,
            'structure': self.structure,
            'price': self.price,
            'image': self.image,
            'type': self.type,
            'status': self.status
        }
        with open(os.path.join(product_folder, 'product.json'), 'w') as json_file:
            json.dump(product_info, json_file)

        # Создание TXT файла
        with open(os.path.join(product_folder, 'product.txt'), 'w') as txt_file:
            txt_file.write(f'Product ID: {self.id}\n')
            txt_file.write(f'Product Name: {self.name}\n')
            txt_file.write(f'Small Description: {self.smallDescription}\n')
            txt_file.write(f'Description: {self.description}\n')
            txt_file.write(f'Application: {self.application}\n')
            txt_file.write(f'Structure: {self.structure}\n')
            txt_file.write(f'Price: {self.price}\n')
            txt_file.write(f'Image: {self.image}\n')
            txt_file.write(f'Type: {self.type}\n')
            txt_file.write(f'Status: {self.status}\n')

        # Загрузка изображения (если есть)
        if self.image:
            image_path = os.path.join(product_folder, os.path.basename(self.image))
            
            if self.image.startswith('http://') or self.image.startswith('https://'):
                
                # Если ссылка не содержит в себе типа изображения,
                # то конвертируем его автоматически в .jpg
                if not self.image.endswith('.jpg') or \
                    not self.image.endswith('.jpeg') or \
                    not self.image.endswith('.png'):
                        
                    if image_path[:-1] == '/':
                        image_path = image_path[:-1]
                        
                    image_path +='.jpg'
                    
                import requests
                
                # Загрузка изображения из интернета
                response = requests.get(self.image)
                with open(image_path, 'wb') as img_file:
                     img_file.write(response.content)
                    
            else:
                
                import shutil
                
                # Копирование изображения из локальной файловой системы
                shutil.copy(self.image, image_path)

            # Сохранение ссылки на изображение в базе данных
            self.image = image_path
            
    def calculate_sale_price(self, discount_percentage: float) -> float:
        """
        Calculate the sale price based on the discount percentage.
        @params discount_percentage: The discount percentage to apply.
        @return: The calculated sale price.
        """
        if self.is_on_sale:
            return self.price * (1 - discount_percentage / 100)
        return self.price