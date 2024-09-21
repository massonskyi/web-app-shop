import logging
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

from core import cfg

async_engine = None
AsyncSessionLocal = None
Base = declarative_base()

async def init_db():
    global async_engine, AsyncSessionLocal

    logging.info("Initializing the database...")

    if async_engine is None:
        try:
            # Create async engine
            logging.info(f"Creating async engine with URL: {cfg['DATABASE_URL']}")
            async_engine = create_async_engine(cfg["DATABASE_URL"], echo=True)

            # Create session factory
            logging.info("Creating session factory...")
            AsyncSessionLocal = sessionmaker(
                bind=async_engine,
                class_=AsyncSession,
                autocommit=False,
                autoflush=False,
                expire_on_commit=False
            )

            logging.info("Database initialized successfully.")
        except SQLAlchemyError as e:
            logging.error(f"Error initializing the database: {e}")
            raise

    if AsyncSessionLocal is None:
        logging.error("AsyncSessionLocal is still None after init_db().")
        raise RuntimeError("AsyncSessionLocal was not properly initialized")
