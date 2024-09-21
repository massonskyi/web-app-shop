from datetime import (
    datetime, 
    timedelta
)

from typing import Any
from jose import JWTError, jwt



from fastapi import(
    Depends, 
    HTTPException,
    status
)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from middleware.apps.admin.schemas import TokenData
from middleware.apps.admin import oauth2_scheme

from middleware.apps.admin.models import Admin
from database.session import get_async_db
from core import cfg
from middleware.apps.admin import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM

def create_access_token(
        data: dict,
        expires_delta=None,
) -> tuple[str, datetime | Any]:
    """
    Create an access token with the given data and expiration time.

    Args:
        data: A dictionary containing the data to be encoded in the token.
        expires_delta: The expiration time for the token. If not provided, the token will expire after 30 minutes.
        ACCESS_TOKEN_EXPIRE_MINUTES: int = 999,
        ALGORITHM: str = "HS256"
    Returns:
        The encoded access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, cfg['BACKEND_SECRET_COOKIE_KEY'], algorithm=ALGORITHM)
    return encoded_jwt, expire


async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: AsyncSession = Depends(get_async_db)
) -> Admin:
    """
    Get the current user. If the token is valid, return the user.
    Args:
        token: str = Depends(oauth2_scheme), The token to validate. 
        db: AsyncSession = Depends(get_async_db) The database session.
    Returns:
        The current user. If the token is invalid, return None.
    """
    try:
        payload = jwt.decode(token, cfg['BACKEND_SECRET_COOKIE_KEY'], algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        
        if user_id is None:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: User ID is not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
            
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await db.execute(select(Admin).filter(Admin.id == user_id))
    user = user.scalars().first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: Admin not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# Функция для проверки JWT токена
def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, cfg['BACKEND_SECRET_COOKIE_KEY'], algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data