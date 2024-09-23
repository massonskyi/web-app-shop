


import json
from typing import List
from fastapi import(
     APIRouter,
     Depends,
     HTTPException, 
     Response,
)

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_async_db
from middleware.apps.admin.manager import AdminManager
from middleware.apps.admin.models import Admin
from middleware.apps.admin.schemas import AdminCreateScheme, AdminSignInScheme, AdminUpdateScheme
from middleware.apps.admin.utils import get_current_user


API_ADMIN_MODULE = APIRouter(
    prefix="/admins",
    tags=["Admin CRUD API"]
)

AdminSignInResponse = AdminSignInScheme
AdminCreateResponse = AdminCreateScheme
AdminUpdateResponse = AdminUpdateScheme


@API_ADMIN_MODULE.post(
    '/sign_in',
    response_model = AdminSignInResponse,
    summary="Sign in admin"
)
async def sign_in(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db:AsyncSession = Depends(get_async_db)
) -> None:
    """
    Sign in an admin.

    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing the username and password.
        db (AsyncSession): The database session.

    Returns:
        AdminSignInSchema: The signed-in admin with an access token.

    Raises:
        HTTPException: If the admin is not found or the password is invalid.
    """

    manager = AdminManager(db)
    admin_sign_in_schema = AdminSignInResponse(username=form_data.username, password=form_data.password)
    admin,token,expire = await manager.sign_in_admin(admin_sign_in_schema)
    
        # Create JSON response content
    response_content = {
        "admin": admin.dict(),  # Convert user object to dictionary
        "message": "Sign in admin successfully",
        "access_token": token,
        "token_type": "bearer",
        "token_expires_at": expire.timestamp()  # Convert datetime to ISO format string
    }
    response_json = json.dumps(response_content)  # Convert dictionary to JSON string
    response = Response(content=response_json, media_type="application/json")

    # Set the cookie
    response.set_cookie(
        key="access_token",
        value=token,
        expires=expire.timestamp(),  # Convert datetime to timestamp
        secure=False,  # Optional: Set Secure flag if using HTTPS
        httponly=False,  # Optional: Set the HttpOnly flag for security
        samesite=None, # Optional: Set SameSite policy
        path="/",  # Ensure the cookie is available throughout your site
    )
    return response


@API_ADMIN_MODULE.post(
    '/',
    response_model = AdminCreateResponse,
    summary="Create a new admin"
)
async def create_admin(
    admin: AdminCreateResponse,
    db: AsyncSession = Depends(get_async_db), 
)->None:
    """
    Create a new admin.
pass321S#
    Args:
        admin (AdminCreateSchema): The admin data to create.
        db (AsyncSession): The database session.
        current_user (Admin): The current authenticated user.

    Returns:
        AdminCreateSchema: TheUser created successfully created admin.

    Raises:
        HTTPException: If the admin data is invalid or an error occurs.
    """
    admin_manager = AdminManager(db)
    admin,token,expire = await admin_manager.create_new_admin(admin)
    # Create JSON response content
    response_content = {
        "admin": admin.dict(),  # Convert user object to dictionary
        "message": "Admin created successfully",
        "access_token": token,
        "token_type": "bearer",
        "token_expires_at": expire.isoformat()  # Convert datetime to ISO format string
    }
    response_json = json.dumps(response_content)  # Convert dictionary to JSON string
    response = Response(content=response_json, media_type="application/json")

    # Set the cookie
    response.set_cookie(
        key="access_token",
        value=token,
        expires=expire.timestamp(),  # Convert datetime to timestamp
        secure=False,  # Optional: Set Secure flag if using HTTPS
        httponly=True,  # Optional: Set the HttpOnly flag for security
        samesite=None, # Optional: Set SameSite policy
        path="/",  # Ensure the cookie is available throughout your site
        domain="localhost"  # Adjust this if your site spans multiple subdomains
    )
    return response

@API_ADMIN_MODULE.get(
    '/gets/',
    response_model = List[AdminCreateResponse],
    summary="Get all admins"
)
async def read_admins(
    db: AsyncSession = Depends(get_async_db), 
    current_user: Admin = Depends(get_current_user)
) -> None:
    """
    Get all admins.

    Args:
        db (AsyncSession): The database session.
        current_user (Admin): The current authenticated user.

    Returns:
        List[AdminCreateSchema]: A list of all admins.

    Raises:
        HTTPException: If an error occurs.
    """
    admin_manager = AdminManager(db)
    admins = await admin_manager.get_all_admins()
    
    # Create JSON response content
    response_content = {
        "admins":admins,  # Convert user object to dictionary
        "message": "Get admins successfully",
    }
    response_json = json.dumps(response_content)  # Convert dictionary to JSON string
    response = Response(content=response_json, media_type="application/json")

    return response

@API_ADMIN_MODULE.get(
    "/{admin_id}",
    response_model = AdminCreateScheme,
    summary="Get an admin by ID"
)
async def read_admin(
    admin_id: int, 
    db: AsyncSession = Depends(get_async_db), 
    current_user: Admin = Depends(get_current_user)
) -> None:
    """
    Get an admin by ID.

    Args:
        admin_id (int): The ID of the admin to retrieve.
        db (AsyncSession): The database session.
        current_user (Admin): The current authenticated user.

    Returns:
        AdminCreateSchema: The admin with the specified ID.

    Raises:
        HTTPException: If the admin is not found or an error occurs.
    """
    admin_manager = AdminManager(db)
    admin = await admin_manager.get_admin(admin_id)
    if admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    # Create JSON response content
    response_content = {
        "admin": admin.dict(),  # Convert user object to dictionary
        "message": "Get admin successfully",
    }
    response_json = json.dumps(response_content)  # Convert dictionary to JSON string
    response = Response(content=response_json, media_type="application/json")
    
    return response

@API_ADMIN_MODULE.put(
    "/{admin_id}",
    response_model = AdminCreateResponse,
    summary="Update an admin by ID"
)
async def update_admin(
    admin_id: int, 
    update: AdminUpdateResponse, 
    db: AsyncSession = Depends(get_async_db), 
    current_user: Admin = Depends(get_current_user)
) -> None:
    """
    Update an admin by ID.

    Args:
        admin_id (int): The ID of the admin to update.
        update (AdminUpdateSchema): The updated admin data.
        db (AsyncSession): The database session.
        current_user (Admin): The current authenticated user.

    Returns:
        AdminCreateSchema: The updated admin.

    Raises:
        HTTPException: If the admin is not found or an error occurs.
    """
    admin_manager = AdminManager(db)
    updated_admin = await admin_manager.update_admin(admin_id, update)
    if updated_admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    # Create JSON response content
    response_content = {
        "admin": updated_admin.dict(),  # Convert user object to dictionary
        "message": "Admin updated successfully",
    }
    response_json = json.dumps(response_content)  # Convert dictionary to JSON string
    response = Response(content=response_json, media_type="application/json")
    
    return response

@API_ADMIN_MODULE.delete(
    "/{admin_id}",
    response_model = AdminCreateResponse,
    summary="Delete an admin by ID"
)
async def delete_admin(
    admin_id: int, 
    db: AsyncSession = Depends(get_async_db), 
    current_user: Admin = Depends(get_current_user)
) -> None:
    """
    Delete an admin by ID.

    Args:
        admin_id (int): The ID of the admin to delete.
        db (AsyncSession): The database session.
        current_user (Admin): The current authenticated user.

    Returns:
        dict: A message indicating that the admin was deleted.

    Raises:
        HTTPException: If the admin is not found or an error occurs.
    """
    admin_manager = AdminManager(db)
    await admin_manager.delete_admin(admin_id)
    # Create JSON response content
    response_content = {
        "message": "Admin deleted successfully",
    }
    response_json = json.dumps(response_content)  # Convert dictionary to JSON string
    response = Response(content=response_json, media_type="application/json")
    
    return response
