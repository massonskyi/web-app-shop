import shutil
from typing import (
    List, 
    Optional
)
import json
from typing_extensions import deprecated
from fastapi import (
    APIRouter, 
    Depends,
    File, 
    Form,
    HTTPException,
    UploadFile, 
    status as HTTPStatus, 
    Response
)
from fastapi.responses import JSONResponse
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
DEFAULT_IMAGE_PATH: Optional[str] = f"../../../../../frontend/build/static/uploads/default.png"
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
    summary='Create product',
)
async def create_product(
    new: CreateProductResponse = Depends(),
    product_manager: 'ProductManager' = Depends(get_product_manager),
    current_user: Admin = Depends(get_current_user)
) -> Response:
    """
    Create product. API endpoint.
    """

    response_content = {}
    status_code: HTTPStatus
    if new.file:
        file_name = f"file_{new.name}_{new.file.filename}"
        file_path = f"D:\\study\\уник\\web\\web-app-shop\\frontend\\build\\static\\uploads\\{file_name}"

        # save
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(new.file.file, buffer)

        result_image_path = file_path
    else:
        result_image_path = DEFAULT_IMAGE_PATH

    try:

        new_product = await product_manager.create_new_product(new, image=result_image_path)
    except Exception as e:
        status_code = HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status_code,
            detail=str(e)
        )
    else:
        response_content['product'] = new_product
        response_content['detail'] = "Successfully created product "
        status_code = HTTPStatus.HTTP_201_CREATED  # 201 Created
    finally:
        if not response_content.get('product', None):
            response_content['product'] = None
            response_content['detail'] = "Failed to create product"
            status_code = HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR # 500 Internal Server Error

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
    status_code: HTTPStatus
    try:
        product, file = await product_manager.get_product_by_id(product_id)
    except Exception as e:
        status_code = HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status_code,
            detail=str(e)
        )
    else:
        response_content['product'] = product  # Исключаем объект файла
        response_content['file'] = file
        response_content['details'] = "Successfully get product"
        status_code = HTTPStatus.HTTP_202_ACCEPTED  # 202 Accepted   
    finally:
        
        if not response_content.get('product', None):
            response_content['product'] = None
            response_content['details'] = "Failed to get product"
            status_code = HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR # 500 Internal Server Error
            
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
    status_code: HTTPStatus
    try:
        products = await product_manager.get_all_products()
    except Exception as e:
        status_code = HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status_code,
            detail=str(e)
        )
    else:
        response_content['products'] = {"all_products":products} 
        response_content['details'] = "Successfully get all products"
        status_code = HTTPStatus.HTTP_202_ACCEPTED  # 202 Accepted   
    finally:
        
        if not response_content.get('products', None):
            response_content['products'] = None
            response_content['details'] = "Failed to get all products"
            status_code = HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR # 500 Internal Server Error
        
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
    status_code: HTTPStatus
    try:
        products = await product_manager.get_products_by_type(product_type)
    except Exception as e:
        status_code = HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status_code,
            detail=str(e)
        )
    else:
        response_content['products'] = {"all_products":products} 
        response_content['details'] = "Successfully get all products"
        status_code = HTTPStatus.HTTP_202_ACCEPTED  # 202 Accepted   
    finally:
        
        if not response_content.get('products', None):
            response_content['products'] = None
            response_content['details'] = "Failed to get all products"
            status_code = HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR # 500 Internal Server Error
        
    response_json = json.dumps(response_content)  # Convert dictionary to JSON string
    response = Response(content=response_json, media_type="application/json", status_code=status_code)
    return response

@API_PRODUCT_MODULE.put(
    '/{product_id}',
    summary='Update product by id',
)
async def update_product_by_id(
    product_id: int,
    product: CreateProductResponse = Depends(),
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
    status_code: HTTPStatus
    if product.file:
        file_name = f"file_{product.name}_{product.file.filename}"
        file_path = f"D:\\study\\уник\\web\\web-app-shop\\frontend\\build\\static\\uploads\\{file_name}"

        # save
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(product.file.file, buffer)

        result_image_path = file_path
    else:
        result_image_path = DEFAULT_IMAGE_PATH

    try:
        updated_product = await product_manager.update_product_by_id(product_id, product, result_image_path)
    except Exception as e:
        status_code = HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status_code,
            detail=str(e)
        )
    else:
        response_content['product'] = updated_product
        response_content['details'] = "Successfully updated product"
        status_code = HTTPStatus.HTTP_202_ACCEPTED  # 202 Accepted   
    finally:
        
        if not response_content.get('product', None):
            response_content['product'] = None
            response_content['details'] = "Failed to update product"
            status_code = HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR # 500 Internal Server Error
            
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
    status_code: HTTPStatus
    try:
        deleted_product = await product_manager.delete_product(product_id)
    except Exception as e:
        status_code = HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status_code,
            detail=str(e)
        )
    else:
        response_content['product'] = deleted_product
        response_content['details'] = "Successfully deleted product"
        status_code = HTTPStatus.HTTP_202_ACCEPTED  # 202 Accepted   
    finally:
        
        if not response_content.get('product', None):
            response_content['product'] = None
            response_content['details'] = "Failed to delete product"
            status_code = HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR # 500 Internal Server Error
            
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
    status_code: HTTPStatus
    try:
        products = await product_manager.get_products_on_sale()
    except Exception as e:
        status_code = HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status_code,
            detail=str(e)
        )
    else:
        response_content['products'] = {"all_products":products} 
        response_content['details'] = "Successfully get all products on sale"
        status_code = HTTPStatus.HTTP_202_ACCEPTED  # 202 Accepted
    finally:
        if not response_content.get('products', None):
            response_content['products'] = None
            response_content['details'] = "Failed to get all products on sale"
            status_code = HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR # 500 Internal Server Error

    response_json = json.dumps(response_content)  # Convert dictionary to JSON string
    response = Response(content=response_json, media_type="application/json", status_code=status_code)
    return response



@deprecated("Will be delite on version api 2")
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
    status_code: HTTPStatus
    try:
        products = await product_manager.get_products_with_sale_price()
    except Exception as e:
        status_code = HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status_code,
            detail=str(e)
        )
    else:
        response_content['products'] = [product.dict() for product in products]
        response_content['details'] = "Successfully get all products with sale price"
        status_code = HTTPStatus.HTTP_202_ACCEPTED  # 202 Accepted
    finally:
        if not response_content.get('products', None):
            response_content['products'] = None
            response_content['details'] = "Failed to get all products with sale price"
            status_code = HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR # 500 Internal Server Error

    response_json = json.dumps(response_content)  # Convert dictionary to JSON string
    response = Response(content=response_json, media_type="application/json", status_code=status_code)
    return response