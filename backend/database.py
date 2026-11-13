"""
================================================================================
BACKEND ASYNC POSTGRESQL DATABASE ENGINE & SESSION SETUP
================================================================================
Database: design
Driver: asyncpg (Asynchronous Cython PostgreSQL Driver)
ORM: SQLAlchemy 2.0 AsyncIO
================================================================================
"""

import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# Load variables from .env file
load_dotenv()

# Read from .env, or use PostgreSQL connection for 'design' DB
DEFAULT_URL = "postgresql+asyncpg://postgres:ashish123@localhost:5432/design"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_URL)

# Create Async Engine with connection pooling
engine = create_async_engine(
    DATABASE_URL,
    echo=False,           # Set True if you want raw SQL queries logged in console
    pool_pre_ping=True,   # Pings DB before handing connection to avoid stale sockets
    pool_recycle=300,     # Recycles connection every 5 minutes
)

# Async Session Factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# Declarative Base for all models
class Base(DeclarativeBase):
    pass

# FastAPI Dependency for injecting DB session into endpoints
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()







