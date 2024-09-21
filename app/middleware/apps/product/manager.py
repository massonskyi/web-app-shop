from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from middleware.apps.product.models import Product
from functions.async_logger import AsyncLogger
from .schemas import CreateProductSchema, UpdateProductSchema

class ProductManager:
    """
    Product manager class. This class manages the product database.
    The manager class is responsible for creating, reading, updating and deleting products.
    """

    log = AsyncLogger(__name__)

    def __init__(self, database_session: AsyncSession) -> None:
        """
        Initialize the product manager.
        @params: database_session: The database session.
        @return: None
        @raise: Exception if any errors occur. Raises an exception if any error occurs.
        """
        self.__async_db_session = database_session

    async def create_new_product(self, new: CreateProductSchema) -> Optional[CreateProductSchema]:
        """
        Create a new product.
        @params: new: The new product.
        @return: The new product.
        @raise: Exception if any errors occur. Raises an exception if any error occurs.
        """
        if not new.validate():
            await self.log.b_crit(f"Validation error: {new.errors()}")
            raise ValueError(f"Validation error: {new.errors()}")

        new_product = Product(**new.dict())

        try:
            async with self.__async_db_session as async_session:
                async with async_session.begin():
                    async_session.add(new_product)
                    await async_session.commit()
        except SQLAlchemyError as e:
            await self.log.b_crit(f"Error: {e}")
            raise SQLAlchemyError(f"Error: {e}")

        return CreateProductSchema(**new_product.dict())

    async def get_product_by_id(self, product_id: int) -> Optional[CreateProductSchema]:
        """
        Get a product by its ID.
        @params: product_id: The ID of the product.
        @return: The product if found, None otherwise.
        @raise: Exception if any errors occur. Raises an exception if any error occurs.
        """
        try:
            async with self.__async_db_session as async_session:
                result = await async_session.execute(select(Product).filter_by(id=product_id))
                product = result.scalar_one_or_none()
                if product:
                    return CreateProductSchema(**product.dict())
                return None
        except SQLAlchemyError as e:
            await self.log.b_crit(f"Error: {e}")
            raise SQLAlchemyError(f"Error: {e}")

    async def get_all_products(self) -> List[Optional[CreateProductSchema]]:
        """
        Get all products.
        @return: A list of all products.
        @raise: Exception if any errors occur. Raises an exception if any error occurs.
        """
        try:
            async with self.__async_db_session as async_session:
                result = await async_session.execute(select(Product))
                products = result.scalars().all()
                return [CreateProductSchema(**product.dict()) for product in products]
        except SQLAlchemyError as e:
            await self.log.b_crit(f"Error: {e}")
            raise SQLAlchemyError(f"Error: {e}")

    async def get_products_by_type(self, product_type: str) -> List[Optional[CreateProductSchema]]:
        """
        Get all products by type.
        @params: product_type: The type of the products to retrieve.
        @return: A list of products of the specified type.
        @raise: Exception if any errors occur. Raises an exception if any error occurs.
        """
        try:
            async with self.__async_db_session as async_session:
                result = await async_session.execute(select(Product).filter_by(type=product_type))
                products = result.scalars().all()
                return [CreateProductSchema(**product.dict()) for product in products]
        except SQLAlchemyError as e:
            await self.log.b_crit(f"Error: {e}")
            raise SQLAlchemyError(f"Error: {e}")

    async def get_products_on_sale(self) -> List[Optional[CreateProductSchema]]:
        """
        Get all products that are on sale.
        @return: A list of products that are on sale.
        @raise: Exception if any errors occur. Raises an exception if any error occurs.
        """
        try:
            async with self.__async_db_session as async_session:
                result = await async_session.execute(select(Product).filter_by(is_on_sale=True))
                products = result.scalars().all()
                return [CreateProductSchema(**product.dict()) for product in products]
        except SQLAlchemyError as e:
            await self.log.b_crit(f"Error: {e}")
            raise SQLAlchemyError(f"Error: {e}")

    async def get_products_with_sale_price(self) -> List[Optional[CreateProductSchema]]:
        """
        Get all products and display the sale price if the product is on sale.
        @return: A list of all products with the sale price if applicable.
        @raise: Exception if any errors occur. Raises an exception if any error occurs.
        """
        try:
            async with self.__async_db_session as async_session:
                result = await async_session.execute(select(Product))
                products = result.scalars().all()
                product_list = []
                for product in products:
                    product_dict = product.dict()
                    if product.is_on_sale:
                        product_dict['price'] = product.sale_price
                    product_list.append(CreateProductSchema(**product_dict))
                return product_list
        except SQLAlchemyError as e:
            await self.log.b_crit(f"Error: {e}")
            raise SQLAlchemyError(f"Error: {e}")

    async def update_product_by_id(self, product_id: int, update: UpdateProductSchema) -> Optional[CreateProductSchema]:
        """
        Update a product.
        @params: product_id: The ID of the product to update.
        @params: update: The updated product data.
        @return: The updated product if found, None otherwise.
        @raise: Exception if any errors occur. Raises an exception if any error occurs.
        """
        try:
            async with self.__async_db_session as async_session:
                result = await async_session.execute(select(Product).filter_by(id=product_id))
                product = result.scalar_one_or_none()
                if product:
                    for key, value in update.dict(exclude_unset=True).items():
                        setattr(product, key, value)
                    await async_session.commit()
                    return CreateProductSchema(**product.dict())
                return None
        except SQLAlchemyError as e:
            await self.log.b_crit(f"Error: {e}")
            raise SQLAlchemyError(f"Error: {e}")

    async def delete_product(self, product_id: int) -> bool:
        """
        Delete a product.
        @params: product_id: The ID of the product to delete.
        @return: True if the product was deleted, False otherwise.
        @raise: Exception if any errors occur. Raises an exception if any error occurs.
        """
        try:
            async with self.__async_db_session as async_session:
                async with async_session.begin():
                    result = await async_session.execute(select(Product).filter_by(id=product_id))
                    product = result.scalar_one_or_none()
                    if product:
                        await async_session.delete(product)
                        await async_session.commit()
                        return True
                    return False
        except SQLAlchemyError as e:
            await self.log.b_crit(f"Error: {e}")
            raise SQLAlchemyError(f"Error: {e}")
