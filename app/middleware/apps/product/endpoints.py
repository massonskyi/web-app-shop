import shutil
from typing import (
    List, 
    Optional
)
import json
from fastapi import (
    APIRouter, 
    Depends,
    File, 
    HTTPException,
    UploadFile, 
    status, 
    Response
)
from sqlalchemy.ext.asyncio import AsyncSession

from middleware.apps.admin.models import Admin
from middleware.apps.admin.utils import get_current_user
from middleware.apps.product.manager import ProductManager
from middleware.apps.product.schemas import CreateProductSchema
from database.session import get_async_db

API_PRODUCT_MODULE = APIRouter(
    prefix="/product",
    tags=['Product module API']
)
DEFAULT_IMAGE_PATH: Optional[str] = f"../../../../frontend/build/static/uploads/default.png"
CreateProductResponse = CreateProductSchema

async def get_product_manager(
    db_session: AsyncSession = Depends(get_async_db)   
) -> 'ProductManager':
    """
    Get product manager instance.
    @params:
            db_session: database session. 
    @return:
            product manager instance.  
    
    @raise: HTTPException if product manager instance not found. 
    """
    return ProductManager(db_session)



@API_PRODUCT_MODULE.post(
    '/',
    response_model=CreateProductResponse,
    summary= 'Create product',
)
async def create_product(
    product: CreateProductResponse,
    product_manager: 'ProductManager' = Depends(get_product_manager),
    file: UploadFile = File(...),
    current_user: Admin = Depends(get_current_user)
) -> Response:
    """
    Create product. API endpoint. 
    """
    response_content = {}
    status_code: status
    if file:
        file_name = f"file_{product.name}_{file.filename}"
        file_path = f"../../../../frontend/build/static/uploads/{file_name}"
        
        # save
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        product.image = file_path
    else:
        product.image = DEFAULT_IMAGE_PATH
    
    try:
        new_product = await product_manager.create_new_product(product)
    except Exception as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status_code,
            detail=str(e)
        )
    else:
        response_content['product'] = new_product.dict()
        response_content['detail'] = "Successfully created product "
        status_code = status.HTTP_201_CREATED  # 201 Created    
    finally:

        if not response_content.get('product', None):
            response_content['product'] = None
            response_content['detail'] = "Failed to create product"
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR # 500 Internal Server Error
            
    response_json = json.dumps(response_content)  # Convert dictionary to JSON string
    response = Response(content=response_json, media_type="application/json", status_code=status_code)
    return response
    
@API_PRODUCT_MODULE.get(
    '/{product_id}',
    response_model=CreateProductResponse,
    summary='Get product by id',
)
async def get_product_by_id(
    product_id: int,
    product_manager: 'ProductManager' = Depends(get_product_manager),
) -> Response:
    """
    Get product by id. API endpoint. 
    @params: product_id: product id.
    @params: product_manager: Dependency
    @return: Response object. 
    @raise: HTTPException if product not found.
    """
    response_content = {}
    status_code: status
    try:
        product = await product_manager.get_product_by_id(product_id)
    except Exception as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status_code,
            detail=str(e)
        )
    else:
        response_content['product'] = product.dict()
        response_content['details'] = "Successfully get product"
        status_code = status.HTTP_202_ACCEPTED  # 202 Accepted   
    finally:
        
        if not response_content.get('product', None):
            response_content['product'] = None
            response_content['details'] = "Failed to get product"
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR # 500 Internal Server Error
            
        response_json = json.dumps(response_content)  # Convert dictionary to JSON string
        response = Response(content=response_json, media_type="application/json", status_code=status_code)
        return response


@API_PRODUCT_MODULE.get(
    '/gets/',
    response_model=List[CreateProductResponse],
    summary='Get all products',
)
async def get_all_products(
    product_manager: 'ProductManager' = Depends(get_product_manager),
) -> Response:
    """
    Get all products. API endpoint. 
    @params: product_manager: Dependency
    @return: Response object. 
    @raise: HTTPException if products not found.
    """
    response_content = {}
    status_code: status
    try:
        products = await product_manager.get_all_products()
    except Exception as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status_code,
            detail=str(e)
        )
    else:
        response_content['products'] = [product.dict() for product in products]
        response_content['details'] = "Successfully get all products"
        status_code = status.HTTP_202_ACCEPTED  # 202 Accepted   
    finally:
        
        if not response_content.get('products', None):
            response_content['products'] = None
            response_content['details'] = "Failed to get all products"
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR # 500 Internal Server Error
        
    response_json = json.dumps(response_content)  # Convert dictionary to JSON string
    response = Response(content=response_json, media_type="application/json", status_code=status_code)
    return response

@API_PRODUCT_MODULE.get(
    '/filters/{product_type}',
    response_model=List[CreateProductResponse],
    summary='Get all products',
)
async def get_all_products(
    product_type: str,
    product_manager: 'ProductManager' = Depends(get_product_manager),
) -> Response:
    """
    Get all products. API endpoint. 
    @params: product_manager: Dependency
    @return: Response object. 
    @raise: HTTPException if products not found.
    """
    response_content = {}
    status_code: status
    try:
        products = await product_manager.get_products_by_type(product_type=product_type)
    except Exception as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status_code,
            detail=str(e)
        )
    else:
        if not products:  # If product not found
            pass
        
        response_content['products'] = [product.dict() for product in products]
        response_content['details'] = "Successfully get all products"
        status_code = status.HTTP_202_ACCEPTED  # 202 Accepted   
    finally:
        
        if not response_content.get('products', None):
            response_content['products'] = None
            response_content['details'] = "Failed to get all products"
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR # 500 Internal Server Error
        
    response_json = json.dumps(response_content)  # Convert dictionary to JSON string
    response = Response(content=response_json, media_type="application/json", status_code=status_code)
    return response

@API_PRODUCT_MODULE.put(
    '/{product_id}',
    response_model=CreateProductResponse,
    summary='Update product by id',
)
async def update_product_by_id(
    product_id: int,
    product: CreateProductResponse,
    product_manager: 'ProductManager' = Depends(get_product_manager),
    current_user: Admin = Depends(get_current_user)
) -> Response:
    """
    Update product by id. API endpoint. 
    @params: product_id: product id.
    @params: product: product data.
    @params: product_manager: Dependency
    @return: Response object. 
    @raise: HTTPException if product not found.
    """
    response_content = {}
    status_code: status
    try:
        updated_product = await product_manager.update_product_by_id(product_id, product)
    except Exception as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status_code,
            detail=str(e)
        )
    else:
        response_content['product'] = updated_product.dict()
        response_content['details'] = "Successfully updated product"
        status_code = status.HTTP_202_ACCEPTED  # 202 Accepted   
    finally:
        
        if not response_content.get('product', None):
            response_content['product'] = None
            response_content['details'] = "Failed to update product"
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR # 500 Internal Server Error
            
        response_json = json.dumps(response_content)  # Convert dictionary to JSON string
        response = Response(content=response_json, media_type="application/json", status_code=status_code)
        return response


@API_PRODUCT_MODULE.delete(
    '/{product_id}',
    response_model=CreateProductResponse,
    summary='Delete product by id',
)
async def delete_product_by_id(
    product_id: int,
    product_manager: 'ProductManager' = Depends(get_product_manager),
    current_user: Admin = Depends(get_current_user)
) -> Response:
    """
    Delete product by id. API endpoint. 
    @params: product_id: product id.
    @params: product_manager: Dependency
    @return: Response object. 
    @raise: HTTPException if product not found.
    """
    response_content = {}
    status_code: status
    try:
        deleted_product = await product_manager.delete_product_by_id(product_id)
    except Exception as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status_code,
            detail=str(e)
        )
    else:
        response_content['product'] = deleted_product.dict()
        response_content['details'] = "Successfully deleted product"
        status_code = status.HTTP_202_ACCEPTED  # 202 Accepted   
    finally:
        
        if not response_content.get('product', None):
            response_content['product'] = None
            response_content['details'] = "Failed to delete product"
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR # 500 Internal Server Error
            
        response_json = json.dumps(response_content)  # Convert dictionary to JSON string
        response = Response(content=response_json, media_type="application/json", status_code=status_code)
        return response


    
@API_PRODUCT_MODULE.get(
    '/on-sale/',
    response_model=List[CreateProductResponse],
    summary='Get all products on sale',
)
async def get_products_on_sale(
    product_manager: 'ProductManager' = Depends(get_product_manager),
) -> Response:
    """
    Get all products on sale. API endpoint.
    @params: product_manager: Dependency
    @return: Response object.
    @raise: HTTPException if products not found.
    """
    response_content = {}
    status_code: status
    try:
        products = await product_manager.get_products_on_sale()
    except Exception as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status_code,
            detail=str(e)
        )
    else:
        response_content['products'] = [product.dict() for product in products]
        response_content['details'] = "Successfully get all products on sale"
        status_code = status.HTTP_202_ACCEPTED  # 202 Accepted
    finally:
        if not response_content.get('products', None):
            response_content['products'] = None
            response_content['details'] = "Failed to get all products on sale"
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR # 500 Internal Server Error

    response_json = json.dumps(response_content)  # Convert dictionary to JSON string
    response = Response(content=response_json, media_type="application/json", status_code=status_code)
    return response

@API_PRODUCT_MODULE.get(
    '/with-sale-price/',
    response_model=List[CreateProductResponse],
    summary='Get all products with sale price',
)
async def get_products_with_sale_price(
    product_manager: 'ProductManager' = Depends(get_product_manager),
) -> Response:
    """
    Get all products with sale price. API endpoint.
    @params: product_manager: Dependency
    @return: Response object.
    @raise: HTTPException if products not found.
    """
    response_content = {}
    status_code: status
    try:
        products = await product_manager.get_products_with_sale_price()
    except Exception as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status_code,
            detail=str(e)
        )
    else:
        response_content['products'] = [product.dict() for product in products]
        response_content['details'] = "Successfully get all products with sale price"
        status_code = status.HTTP_202_ACCEPTED  # 202 Accepted
    finally:
        if not response_content.get('products', None):
            response_content['products'] = None
            response_content['details'] = "Failed to get all products with sale price"
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR # 500 Internal Server Error

    response_json = json.dumps(response_content)  # Convert dictionary to JSON string
    response = Response(content=response_json, media_type="application/json", status_code=status_code)
    return response