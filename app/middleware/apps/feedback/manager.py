from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

from typing import (
    List,
    Union,
    Tuple
)

from middleware.apps.feedback.models import FeedBack
from functions.async_logger import AsyncLogger

from .schemas import *




class FeedBackManager:
    """
    Feedback manager class. This class manages the admin database.
    The manager class is repsponsible for managing the database.
    """
    
    log = AsyncLogger(__name__)
    def __init__(
        self,
        database_session: AsyncSession
    ) -> None:
        """
        Initialize the feedback manager
        @params database_session: database session is AsyncSession object for the database
        @return: None
        @raise: Exception if database session is not initialized
        """
        
        self.__async_db_session = database_session
    
    async def create_feedback(
        self,
        new: CreateFeedBackSchema
    ) -> CreateFeedBackSchema:
        """
        Create a new feedback
        @params new: CreateFeedBackSchema object
        @return: CreateFeedBackSchema object
        @raise: Exception if database session is not initialized
        """
        if not new.validate():
            await self.log.b_crit(f"Validation failed: {new.errors}")
            raise ValueError(f"Validation failed: {new.errors}")
        try:
            new_feedback = FeedBack(**new.dict())
        except:
            raise Exception("РАЗРАБ ДОЛБАЕБ УХЙ!")
        try:
            async with self.__async_db_session as async_session:
                async with async_session.begin():
                    async_session.add(new_feedback)
                    await async_session.commit()
        except SQLAlchemyError as e:
            await self.log.b_crit(f"Failed to create feedback: {e}")
            raise SQLAlchemyError(f"Failed to create feedback: {e}")
        
        return CreateFeedBackSchema(**new_feedback.dict())
    async def get_feedback_by_id(
        self,
        feedback_id: int
    ) -> Optional[CreateFeedBackSchema]:
        """
        Get feedback by ID.
        @params feedback_id: The ID of the feedback to retrieve.
        @return: CreateFeedBackSchema object if found, None otherwise.
        @raise: Exception if any error occurs.
        """
        try:
            async with self.__async_db_session as async_session:
                result = await async_session.execute(select(FeedBack).filter_by(id=feedback_id))
                feedback = result.scalar_one_or_none()
                if feedback:
                    return CreateFeedBackSchema(**feedback.dict())
                return None
        except SQLAlchemyError as e:
            await self.log.b_crit(f"Error: {e}")
            raise SQLAlchemyError(f"Error: {e}")

    async def get_all_feedbacks(self) -> List[Optional[CreateFeedBackSchema]]:
        """
        Get all feedbacks.
        @return: A list of all feedbacks.
        @raise: Exception if any error occurs.
        """
        try:
            async with self.__async_db_session as async_session:
                result = await async_session.execute(select(FeedBack))
                feedbacks = result.scalars().all()
                return [CreateFeedBackSchema(**feedback.dict()) for feedback in feedbacks]
        except SQLAlchemyError as e:
            await self.log.b_crit(f"Error: {e}")
            raise SQLAlchemyError(f"Error: {e}")

    async def update_feedback_by_id(
        self,
        feedback_id: int,
        update: UpdateFeedBackSchema
    ) -> Optional[CreateFeedBackSchema]:
        """
        Update a feedback.
        @params feedback_id: The ID of the feedback to update.
        @params update: The updated feedback data.
        @return: The updated feedback if found, None otherwise.
        @raise: Exception if any error occurs.
        """
        try:
            async with self.__async_db_session as async_session:
                result = await async_session.execute(select(FeedBack).filter_by(id=feedback_id))
                feedback = result.scalar_one_or_none()
                if feedback:
                    for key, value in update.dict(exclude_unset=True).items():
                        setattr(feedback, key, value)
                    await async_session.commit()
                    return CreateFeedBackSchema(**feedback.dict())
                return None
        except SQLAlchemyError as e:
            await self.log.b_crit(f"Error: {e}")
            raise SQLAlchemyError(f"Error: {e}")

    async def delete_feedback_by_id(
        self,
        feedback_id: int
    ) -> bool:
        """
        Delete a feedback by ID.
        @params feedback_id: The ID of the feedback to delete.
        @return: True if the feedback was deleted, False otherwise.
        @raise: Exception if any error occurs.
        """
        try:
            async with self.__async_db_session as async_session:
                result = await async_session.execute(select(FeedBack).filter_by(id=feedback_id))
                feedback = result.scalar_one_or_none()
                if feedback:
                    await async_session.delete(feedback)
                    await async_session.commit()
                    return True
                return False
        except SQLAlchemyError as e:
            await self.log.b_crit(f"Error: {e}")
            raise SQLAlchemyError(f"Error: {e}")