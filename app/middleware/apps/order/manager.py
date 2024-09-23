from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

from typing import List, Optional

from middleware.apps.order.models import Order
from functions.async_logger import AsyncLogger

from .schemas import CreateOrderSchema, UpdateOrderSchema

class OrderManager:
    """
    Order manager class. This class manages the order database.
    The manager class is responsible for managing the database.
    """

    log = AsyncLogger(__name__)

    def __init__(self, database_session: AsyncSession) -> None:
        """
        Initialize the order manager.
        @params database_session: database session is AsyncSession object for the database.
        @return: None
        @raise: Exception if database session is not initialized.
        """
        self.__async_db_session = database_session

    async def create_order(self, new: CreateOrderSchema) -> CreateOrderSchema:
        """
        Create a new order.
        @params new: CreateOrderSchema object.
        @return: CreateOrderSchema object.
        @raise: Exception if database session is not initialized.
        """
        new_order = Order(**new.dict())
        try:
            async with self.__async_db_session as async_session:
                async with async_session.begin():
                    async_session.add(new_order)
                    await async_session.commit()
        except SQLAlchemyError as e:
            await self.log.b_crit(f"Failed to create order: {e}")
            raise SQLAlchemyError(f"Failed to create order: {e}")

        return CreateOrderSchema(**new_order.dict())

    async def get_order_by_id(self, order_id: int) -> Optional[CreateOrderSchema]:
        """
        Get order by ID.
        @params order_id: The ID of the order to retrieve.
        @return: CreateOrderSchema object if found, None otherwise.
        @raise: Exception if any error occurs.
        """
        try:
            result = await self.__async_db_session.execute(select(Order).filter_by(id=order_id))
            order = result.scalar_one_or_none()
            if order:
                return CreateOrderSchema(**order.dict())
            return None
        except SQLAlchemyError as e:
            await self.log.b_crit(f"Error: {e}")
            raise SQLAlchemyError(f"Error: {e}")

    async def get_all_orders(self) -> List[Optional[CreateOrderSchema]]:
        """
        Get all orders.
        @return: A list of all orders.
        @raise: Exception if any error occurs.
        """
        try:
            result = await self.__async_db_session.execute(select(Order))
            orders = result.scalars().all()
            return [CreateOrderSchema(**order.dict()) for order in orders]
        except SQLAlchemyError as e:
            await self.log.b_crit(f"Error: {e}")
            raise SQLAlchemyError(f"Error: {e}")

    async def update_order_by_id(self, order_id: int, update: UpdateOrderSchema) -> Optional[CreateOrderSchema]:
        """
        Update an order.
        @params order_id: The ID of the order to update.
        @params update: The updated order data.
        @return: The updated order if found, None otherwise.
        @raise: Exception if any error occurs.
        """
        try:
            result = await self.__async_db_session.execute(select(Order).filter_by(id=order_id))
            order = result.scalar_one_or_none()
            if order:
                for key, value in update.dict(exclude_unset=True).items():
                    setattr(order, key, value)
                await self.__async_db_session.commit()
                await self.__async_db_session.refresh(order)
                return CreateOrderSchema(**order.dict())
            return None
        except SQLAlchemyError as e:
            await self.log.b_crit(f"Error: {e}")
            raise SQLAlchemyError(f"Error: {e}")

    async def delete_order_by_id(self, order_id: int) -> bool:
        """
        Delete an order by ID.
        @params order_id: The ID of the order to delete.
        @return: True if the order was deleted, False otherwise.
        @raise: Exception if any error occurs.
        """
        try:
            result = await self.__async_db_session.execute(select(Order).filter_by(id=order_id))
            order = result.scalar_one_or_none()
            if order:
                await self.__async_db_session.delete(order)
                await self.__async_db_session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            await self.log.b_crit(f"Error: {e}")
            raise SQLAlchemyError(f"Error: {e}")
