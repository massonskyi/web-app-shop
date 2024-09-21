__version__ = '1.0.0'
__doc__ ="""
A package for application admin in API server
"""
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api_version_1/admins/sign_in")


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60