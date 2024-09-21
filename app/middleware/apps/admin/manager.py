from typing import (
    Union,
    Tuple
)
from sqlalchemy import select
from functions.async_logger import AsyncLogger
from middleware.apps.admin import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM
)
from middleware.apps.admin.models import Admin

from utils import  (
    PasswordManager as pm, 
)

from .utils import(
    create_access_token
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError


from .schemas import (
    AdminCreateScheme,
    AdminSignInScheme,
    AdminUpdateScheme
)
class AdminManager:
    """
    Admin manager class. This class manages the admin database. 
    The manager class is responsible for managing the admin database.
    
    """

    log = AsyncLogger(__name__)
    def __init__(
        self, 
        database_session: AsyncSession
    )->None:
        """
        Initialize the admin manager.
        @params: database_session: AsyncSession object for the admin database.
        @return: None
        @raise: Exception if any error occurs. Raises an exception.
        """
        self.__async_db_session = database_session
        self.pwd = pm()
    async def create_new_admin(
        self,
        new: AdminCreateScheme
    ) -> Tuple[AdminCreateScheme, str, str]:
        """
        Create new admin.
        This method creates a new admin. 
        This method is responsible for creating a new admin.
        @params: new: AdminCreateScheme object for the new admin.
        @return: AdminCreateScheme object for the new admin.
        @raise: Exception if any error occurs. Raises an exception.
        """
        if not new.validate():
            await self.log.b_crit(f"Validation Error: {new.errors}")
            raise ValueError(f"Validation Error: {new.errors}")
        
        hashed_password = self.pwd.hash(new.password)
        
        # Exclude the password field from the dictionary
        new_dict = new.dict(exclude={'password'})

        # Add the hashed password to the dictionary
        new_dict['password'] = hashed_password

        # Create a new Admin instance
        new_admin = Admin(**new_dict)
        
        try:
            async with self.__async_db_session as async_session:
                async with async_session.begin():
                    async_session.add(new_admin)
                    await async_session.commit()
        except SQLAlchemyError as err_sql:
            await self.log.b_crit(f"SQLAlchemy Error: {err_sql}")
            raise SQLAlchemyError(f"SQLAlchemy Error: {err_sql}")
        
        except Exception as err:
            await self.log.b_crit(f"Exception: {err}")
            raise Exception(f"Exception: {err}")
        
        try:
            async with self.__async_db_session as async_session:
                new_added_admin = await async_session.execute(select(Admin)
                                                   .filter(Admin.username == new_admin.username)
                                                   )
                new_added_admin = new_added_admin.scalars().first()
                if not new_added_admin:
                    await self.log.b_crit(f"User not found: {new_admin.username}")
                    raise Exception(f"User not found: {new_admin.username}")
        except SQLAlchemyError as err_sql:
            await self.log.b_crit(f"SQLAlchemy Error: {err_sql}")
            raise SQLAlchemyError(f"SQLAlchemy Error: {err_sql}")
        
        except Exception as err:
            await self.log.b_crit(f"Exception: {err}")
            raise Exception(f"Exception: {err}")
        else:
            access_token, expire = create_access_token(
                data={"sub": str(new_added_admin.id)},
            )
            if not access_token:
                await self.log.b_crit(f"Error creating access token")
                raise Exception(f"Error creating access token")
            if access_token[0] == str(''):
                await self.log.b_crit(f"Error creating access token")
                raise Exception(f"Error creating access token")
            await self.log.b_info(f"Access Token: {access_token}")
            return AdminCreateScheme(**new_added_admin.dict()),access_token,expire
        
    async def sign_in_admin(self, response: AdminSignInScheme) -> Tuple[AdminSignInScheme, str, str]:
        """
        sign in admin. This method signs in an admin. 
        
        Args:
            response: AdminSignInScheme object for the admin to sign in.
            
        Returns:
            AdminSignInScheme object for the admin to sign in. Or None if not found. Raises an exception.
            
        """
        if not response.validate():
            await self.log.b_crit(f"Response error: {response.errors}")
            raise ValueError(f"Response error: {response.errors}")
        
        try:
            async with self.__async_db_session as async_session:
                new_added_admin = await async_session.execute(select(Admin).filter(Admin.username == response.username))
                new_added_admin = new_added_admin.scalars().first()
                
                if not new_added_admin:
                    await self.log.b_crit(f"Admin not found: {response.username}")
                    raise Exception(f"Admin not found: {response.username}")
            
                # hashed_password = self.pwd.hash(response.password)
                # await self.log.b_crit(f"response: {hashed_password}\ndatabase: {new_added_admin.password}")
                if not self.pwd.verify(new_added_admin.password, response.password):
                    await self.log.b_crit(f"Invalid password: {response.username}")
                    raise Exception(f"Invalid password: {response.username}")

        except SQLAlchemyError as err_sql:
            await self.log.b_crit(f"SQLAlchemy Error: {err_sql}")
            raise SQLAlchemyError(f"SQLAlchemy Error: {err_sql}")
        
        except Exception as err:
            await self.log.b_crit(f"Exception: {err}")
            raise Exception(f"Exception: {err}")
        
        else:
            access_token, expire = create_access_token(
                data={"sub": str(new_added_admin.id)},
            )
            if not access_token:
                await self.log.b_crit(f"Error creating access token")
                raise Exception(f"Error creating access token")
            if access_token[0] == str(''):
                await self.log.b_crit(f"Error creating access token")
                raise Exception(f"Error creating access token")
            await self.log.b_info(f"Access Token: {access_token}")
            return AdminSignInScheme(**new_added_admin.dict()), access_token,expire
                
    async def get_admin(self, admin_id: int) -> Admin:
        """
        Get admin by ID.
        This method retrieves an admin by their ID.
        @params: admin_id: ID of the admin to retrieve.
        @return: Admin object.
        @raise: Exception if any error occurs. Raises an exception.
        """
        try:
            async with self.__async_db_session as async_session:
                admin = await async_session.execute(select(Admin).filter(Admin.id == admin_id))
                admin = admin.scalars().first()
                if not admin:
                    await self.log.b_crit(f"Admin not found: {admin_id}")
                    raise Exception(f"Admin not found: {admin_id}")
        except SQLAlchemyError as err_sql:
            await self.log.b_crit(f"SQLAlchemy Error: {err_sql}")
            raise SQLAlchemyError(f"SQLAlchemy Error: {err_sql}")
        except Exception as err:
            await self.log.b_crit(f"Exception: {err}")
            raise Exception(f"Exception: {err}")
        else:
            return AdminCreateScheme(**admin.dict())

    async def update_admin(self, admin_id: int, update: AdminUpdateScheme) -> Admin:
        """
        Update admin.
        This method updates an admin's information.
        @params: admin_id: ID of the admin to update.
        @params: update: AdminUpdateSchema object with the updated information.
        @return: Updated Admin object.
        @raise: Exception if any error occurs. Raises an exception.
        """
        if not update.validate():
            await self.log.b_crit(f"Validation Error: {update.errors}")
            raise ValueError(f"Validation Error: {update.errors}")

        try:
            async with self.__async_db_session as async_session:
                admin = await async_session.execute(select(Admin).filter(Admin.id == admin_id))
                admin = admin.scalars().first()
                if not admin:
                    await self.log.b_crit(f"Admin not found: {admin_id}")
                    raise Exception(f"Admin not found: {admin_id}")

                for key, value in update.dict().items():
                    setattr(admin, key, value)

                await async_session.commit()
        except SQLAlchemyError as err_sql:
            await self.log.b_crit(f"SQLAlchemy Error: {err_sql}")
            raise SQLAlchemyError(f"SQLAlchemy Error: {err_sql}")
        except Exception as err:
            await self.log.b_crit(f"Exception: {err}")
            raise Exception(f"Exception: {err}")
        else:
            return AdminUpdateScheme(**admin.dict())

    async def delete_admin(self, admin_id: int) -> None:
        """
        Delete admin.
        This method deletes an admin by their ID.
        @params: admin_id: ID of the admin to delete.
        @return: None
        @raise: Exception if any error occurs. Raises an exception.
        """
        try:
            async with self.__async_db_session as async_session:
                admin = await async_session.execute(select(Admin).filter(Admin.id == admin_id))
                admin = admin.scalars().first()
                if not admin:
                    await self.log.b_crit(f"Admin not found: {admin_id}")
                    raise Exception(f"Admin not found: {admin_id}")

                await async_session.delete(admin)
                await async_session.commit()
        except SQLAlchemyError as err_sql:
            await self.log.b_crit(f"SQLAlchemy Error: {err_sql}")
            raise SQLAlchemyError(f"SQLAlchemy Error: {err_sql}")
        except Exception as err:
            await self.log.b_crit(f"Exception: {err}")
            raise Exception(f"Exception: {err}")
        
    async def get_all_admins(self) -> list[AdminCreateScheme]:
        """
        Get all admins.
        This method retrieves all admins.
        @return: List of Admin objects.
        @raise: Exception if any error occurs. Raises an exception.
        """
        try:
            async with self.__async_db_session as async_session:
                admins = await async_session.execute(select(Admin))
                admins = admins.scalars().all()
        except SQLAlchemyError as err_sql:
            await self.log.b_crit(f"SQLAlchemy Error: {err_sql}")
            raise SQLAlchemyError(f"SQLAlchemy Error: {err_sql}")
        except Exception as err:
            await self.log.b_crit(f"Exception: {err}")
            raise Exception(f"Exception: {err}")
        else:
            self.log.b_info(f"Admins: {admins}")
            admins = [AdminCreateScheme(**admin.dict()).dict() for admin in admins]
            return admins