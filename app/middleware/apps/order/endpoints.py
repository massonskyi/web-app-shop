from typing import List, Optional
import json
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from middleware.apps.admin.models import Admin
from middleware.apps.admin.utils import get_current_user
from middleware.apps.order.manager import OrderManager
from middleware.apps.order.schemas import CreateOrderSchema, UpdateOrderSchema
from database.session import get_async_db

API_ORDER_MODULE = APIRouter(
    prefix="/orders",
    tags=['Order module API']
)

CreateOrderResponse = CreateOrderSchema

async def get_order_manager(
    db_session: AsyncSession = Depends(get_async_db)
) -> 'OrderManager':
    """
    Get order manager instance.
    @params:
            db_session: database session.
    @return:
            order manager instance.

    @raise: HTTPException if order manager instance not found.
    """
    return OrderManager(db_session)

@API_ORDER_MODULE.post(
    '/',
    response_model=CreateOrderResponse,
    summary='Create order',
)
async def create_order(
    order: CreateOrderResponse,
    order_manager: 'OrderManager' = Depends(get_order_manager),
) -> Response:
    """
    Create order. API endpoint.
    """
    response_content = {}
    status_code: status

    try:
        new_order = await order_manager.create_order(order)
    except Exception as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status_code,
            detail=str(e)
        )
    else:
        response_content['order'] = new_order.dict()
        response_content['detail'] = "Successfully created order"
        status_code = status.HTTP_201_CREATED  # 201 Created
    finally:
        if not response_content.get('order', None):
            response_content['order'] = None
            response_content['detail'] = "Failed to create order"
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR # 500 Internal Server Error

    response_json = json.dumps(response_content)  # Convert dictionary to JSON string
    response = Response(content=response_json, media_type="application/json", status_code=status_code)
    return response

@API_ORDER_MODULE.get(
    '/{order_id}',
    response_model=CreateOrderResponse,
    summary='Get order by id',
)
async def get_order_by_id(
    order_id: int,
    order_manager: 'OrderManager' = Depends(get_order_manager),
    current_user: Admin = Depends(get_current_user)
) -> Response:
    """
    Get order by id. API endpoint.
    @params: order_id: order id.
    @params: order_manager: Dependency
    @return: Response object.
    @raise: HTTPException if order not found.
    """
    response_content = {}
    status_code: status
    try:
        order = await order_manager.get_order_by_id(order_id)
    except Exception as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status_code,
            detail=str(e)
        )
    else:
        response_content['order'] = order.dict()
        response_content['details'] = "Successfully get order"
        status_code = status.HTTP_202_ACCEPTED  # 202 Accepted
    finally:
        if not response_content.get('order', None):
            response_content['order'] = None
            response_content['details'] = "Failed to get order"
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR # 500 Internal Server Error

        response_json = json.dumps(response_content)  # Convert dictionary to JSON string
        response = Response(content=response_json, media_type="application/json", status_code=status_code)
        return response

@API_ORDER_MODULE.get(
    '/gets/',
    response_model=List[CreateOrderResponse],
    summary='Get all orders',
)
async def get_all_orders(
    order_manager: 'OrderManager' = Depends(get_order_manager),
    current_user: Admin = Depends(get_current_user)
) -> Response:
    """
    Get all orders. API endpoint.
    @params: order_manager: Dependency
    @return: Response object.
    @raise: HTTPException if orders not found.
    """
    response_content = {}
    status_code: status
    try:
        orders = await order_manager.get_all_orders()
    except Exception as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status_code,
            detail=str(e)
        )
    else:
        response_content['orders'] = [order.dict() for order in orders]
        response_content['details'] = "Successfully get all orders"
        status_code = status.HTTP_202_ACCEPTED  # 202 Accepted
    finally:
        if not response_content.get('orders', None):
            response_content['orders'] = None
            response_content['details'] = "Failed to get all orders"
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR # 500 Internal Server Error

    response_json = json.dumps(response_content)  # Convert dictionary to JSON string
    response = Response(content=response_json, media_type="application/json", status_code=status_code)
    return response

@API_ORDER_MODULE.put(
    '/{order_id}',
    response_model=CreateOrderResponse,
    summary='Update order by id',
)
async def update_order_by_id(
    order_id: int,
    order: UpdateOrderSchema,
    order_manager: 'OrderManager' = Depends(get_order_manager),
    current_user: Admin = Depends(get_current_user)
) -> Response:
    """
    Update order by id. API endpoint.
    @params: order_id: order id.
    @params: order: order data.
    @params: order_manager: Dependency
    @return: Response object.
    @raise: HTTPException if order not found.
    """
    response_content = {}
    status_code: status
    try:
        updated_order = await order_manager.update_order_by_id(order_id, order)
    except Exception as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status_code,
            detail=str(e)
        )
    else:
        response_content['order'] = updated_order.dict()
        response_content['details'] = "Successfully updated order"
        status_code = status.HTTP_202_ACCEPTED  # 202 Accepted
    finally:
        if not response_content.get('order', None):
            response_content['order'] = None
            response_content['details'] = "Failed to update order"
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR # 500 Internal Server Error

        response_json = json.dumps(response_content)  # Convert dictionary to JSON string
        response = Response(content=response_json, media_type="application/json", status_code=status_code)
        return response

@API_ORDER_MODULE.delete(
    '/{order_id}',
    response_model=CreateOrderResponse,
    summary='Delete order by id',
)
async def delete_order_by_id(
    order_id: int,
    order_manager: 'OrderManager' = Depends(get_order_manager),
    current_user: Admin = Depends(get_current_user)
) -> Response:
    """
    Delete order by id. API endpoint.
    @params: order_id: order id.
    @params: order_manager: Dependency
    @return: Response object.
    @raise: HTTPException if order not found.
    """
    response_content = {}
    status_code: status
    try:
        deleted_order = await order_manager.delete_order_by_id(order_id)
    except Exception as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status_code,
            detail=str(e)
        )
    else:
        response_content['order'] = deleted_order.dict()
        response_content['details'] = "Successfully deleted order"
        status_code = status.HTTP_202_ACCEPTED  # 202 Accepted
    finally:
        if not response_content.get('order', None):
            response_content['order'] = None
            response_content['details'] = "Failed to delete order"
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR # 500 Internal Server Error

        response_json = json.dumps(response_content)  # Convert dictionary to JSON string
        response = Response(content=response_json, media_type="application/json", status_code=status_code)
        return response
