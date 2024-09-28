from typing import List, Optional
import json
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from middleware.apps.admin.models import Admin
from middleware.apps.admin.utils import get_current_user
from middleware.apps.feedback.manager import FeedBackManager
from middleware.apps.feedback.schemas import CreateFeedBackSchema, UpdateFeedBackSchema
from database.session import get_async_db


API_FEEDBACK_MODULE = APIRouter(
    prefix="/feedback",
    tags=['Feedback module API']
)

CreateFeedBackResponse = CreateFeedBackSchema

async def get_feedback_manager(
    db_session: AsyncSession = Depends(get_async_db)
) -> 'FeedBackManager':
    """
    Get feedback manager instance.
    @params:
            db_session: database session.
    @return:
            feedback manager instance.

    @raise: HTTPException if feedback manager instance not found.
    """
    return FeedBackManager(db_session)

@API_FEEDBACK_MODULE.post(
    '/',
    response_model=CreateFeedBackResponse,
    summary='Create feedback',
)
async def create_feedback(
    feedback: CreateFeedBackResponse = Depends(),
    feedback_manager: 'FeedBackManager' = Depends(get_feedback_manager),
) -> Response:
    """
    Create feedback. API endpoint.
    """
    response_content = {}
    status_code: status

    try:
        new_feedback = await feedback_manager.create_feedback(feedback)
    except Exception as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status_code,
            detail=str(e)
        )
    else:
        response_content['feedback'] = new_feedback
        response_content['detail'] = "Successfully created feedback"
        status_code = status.HTTP_201_CREATED  # 201 Created
    finally:
        if not response_content.get('feedback', None):
            response_content['feedback'] = None
            response_content['detail'] = "Failed to create feedback"
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR # 500 Internal Server Error

    response_json = json.dumps(response_content)  # Convert dictionary to JSON string
    response = Response(content=response_json, media_type="application/json", status_code=status_code)
    return response

@API_FEEDBACK_MODULE.get(
    '/{feedback_id}',
    response_model=CreateFeedBackResponse,
    summary='Get feedback by id',
)
async def get_feedback_by_id(
    feedback_id: int,
    feedback_manager: 'FeedBackManager' = Depends(get_feedback_manager),
    current_user: Admin = Depends(get_current_user)
) -> Response:
    """
    Get feedback by id. API endpoint.
    @params: feedback_id: feedback id.
    @params: feedback_manager: Dependency
    @return: Response object.
    @raise: HTTPException if feedback not found.
    """
    response_content = {}
    status_code: status
    try:
        feedback = await feedback_manager.get_feedback_by_id(feedback_id)
    except Exception as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status_code,
            detail=str(e)
        )
    else:
        response_content['feedback'] = feedback
        response_content['details'] = "Successfully get feedback"
        status_code = status.HTTP_202_ACCEPTED  # 202 Accepted
    finally:
        if not response_content.get('feedback', None):
            response_content['feedback'] = None
            response_content['details'] = "Failed to get feedback"
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR # 500 Internal Server Error

        response_json = json.dumps(response_content)  # Convert dictionary to JSON string
        response = Response(content=response_json, media_type="application/json", status_code=status_code)
        return response

@API_FEEDBACK_MODULE.get(
    '/gets/',
    response_model=List[CreateFeedBackResponse],
    summary='Get all feedbacks',
)
async def get_all_feedbacks(
    feedback_manager: 'FeedBackManager' = Depends(get_feedback_manager),
    current_user: Admin = Depends(get_current_user)
) -> Response:
    """
    Get all feedbacks. API endpoint.
    @params: feedback_manager: Dependency
    @return: Response object.
    @raise: HTTPException if feedbacks not found.
    """
    response_content = {}
    status_code: status
    try:
        feedbacks = await feedback_manager.get_all_feedbacks()
    except Exception as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status_code,
            detail=str(e)
        )
    else:
        response_content['feedbacks'] = [feedback for feedback in feedbacks]
        response_content['details'] = "Successfully get all feedbacks"
        status_code = status.HTTP_202_ACCEPTED  # 202 Accepted
    finally:
        if not response_content.get('feedbacks', None):
            response_content['feedbacks'] = None
            response_content['details'] = "Failed to get all feedbacks"
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR # 500 Internal Server Error

    response_json = json.dumps(response_content)  # Convert dictionary to JSON string
    response = Response(content=response_json, media_type="application/json", status_code=status_code)
    return response

@API_FEEDBACK_MODULE.put(
    '/{feedback_id}',
    response_model=CreateFeedBackResponse,
    summary='Update feedback by id',
)
async def update_feedback_by_id(
    feedback_id: int,
    feedback: UpdateFeedBackSchema = Depends(),
    feedback_manager: 'FeedBackManager' = Depends(get_feedback_manager),
    current_user: Admin = Depends(get_current_user)
) -> Response:
    """
    Update feedback by id. API endpoint.
    @params: feedback_id: feedback id.
    @params: feedback: feedback data.
    @params: feedback_manager: Dependency
    @return: Response object.
    @raise: HTTPException if feedback not found.
    """
    response_content = {}
    status_code: status
    try:
        updated_feedback = await feedback_manager.update_feedback_by_id(feedback_id, feedback)
    except Exception as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status_code,
            detail=str(e)
        )
    else:
        response_content['feedback'] = updated_feedback
        response_content['details'] = "Successfully updated feedback"
        status_code = status.HTTP_202_ACCEPTED  # 202 Accepted
    finally:
        if not response_content.get('feedback', None):
            response_content['feedback'] = None
            response_content['details'] = "Failed to update feedback"
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR # 500 Internal Server Error

        response_json = json.dumps(response_content)  # Convert dictionary to JSON string
        response = Response(content=response_json, media_type="application/json", status_code=status_code)
        return response

@API_FEEDBACK_MODULE.delete(
    '/{feedback_id}',
    response_model=CreateFeedBackResponse,
    summary='Delete feedback by id',
)
async def delete_feedback_by_id(
    feedback_id: int,
    feedback_manager: 'FeedBackManager' = Depends(get_feedback_manager),
    current_user: Admin = Depends(get_current_user)
) -> Response:
    """
    Delete feedback by id. API endpoint.
    @params: feedback_id: feedback id.
    @params: feedback_manager: Dependency
    @return: Response object.
    @raise: HTTPException if feedback not found.
    """
    response_content = {}
    status_code: status
    try:
        deleted_feedback = await feedback_manager.delete_feedback_by_id(feedback_id)
    except Exception as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status_code,
            detail=str(e)
        )
    else:
        response_content['feedback'] = deleted_feedback
        response_content['details'] = "Successfully deleted feedback"
        status_code = status.HTTP_202_ACCEPTED  # 202 Accepted
    finally:
        if not response_content.get('feedback', None):
            response_content['feedback'] = None
            response_content['details'] = "Failed to delete feedback"
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR # 500 Internal Server Error

        response_json = json.dumps(response_content)  # Convert dictionary to JSON string
        response = Response(content=response_json, media_type="application/json", status_code=status_code)
        return response
