"""
================================================================================
PRODUCTION-GRADE ASYNC POSTGRESQL ENGINE & DRIVER SETUP
================================================================================
ASYNC DRIVER: `asyncpg`
ORM: `SQLAlchemy 2.0 (AsyncIO)`

--------------------------------------------------------------------------------
🔥 WHY ASYNC DRIVER (asyncpg) INSTEAD OF SYNC DRIVER (psycopg2)?
--------------------------------------------------------------------------------
1. THE EVENT LOOP PROBLEM:
   - FastAPI operates on a single-threaded asynchronous Event Loop (asyncio).
   - If you use a synchronous driver like `psycopg2` inside an `async def` endpoint:
     `db.query(User).all()` BLOCKS the entire Python process thread while waiting
     for PostgreSQL network packets to arrive!
   - While blocked, the server CANNOT respond to any other user. Your concurrency drops to 1!

2. THE ASYNC DRIVER ADVANTAGE (asyncpg):
   - With `asyncpg`, when you write: `await session.execute(...)`, Python frees the thread
     and yields execution back to the Event Loop.
   - While PostgreSQL processes the query over the TCP socket, your server handles
     hundreds of other client requests simultaneously!
   - Result: 10x - 50x higher throughput (RPS) and lower p99 latency.

3. BENCHMARKS:
   - `asyncpg` is written in Cython and uses the raw PostgreSQL binary protocol directly.
   - It is significantly faster than standard synchronous drivers and even beats Go/NodeJS drivers.

--------------------------------------------------------------------------------
🔌 URL DIALECT SCHEMA:
- Synchronous driver URL:  `postgresql://user:pass@host/db` (Uses psycopg2)
- Asynchronous driver URL: `postgresql+asyncpg://user:pass@host/db` (Uses asyncpg)
================================================================================
"""

import os
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

# Load configuration from .env file
load_dotenv()


def get_normalized_database_url() -> str:
    """
    Reads DATABASE_URL from .env and automatically normalizes it for `asyncpg`.

    Why is this needed?
    - Cloud databases (Neon, Supabase, Render, Railway, Aiven) give connection
      strings starting with `postgresql://` or `postgres://`.
    - If passed directly to SQLAlchemy Async, it errors out because it defaults to sync `psycopg2`.
    - Furthermore, `asyncpg` expects `?ssl=require` instead of `?sslmode=require`.
    This function sanitizes the URL so the developer can just copy-paste their link!
    """
    raw_url = os.getenv("DATABASE_URL") or os.getenv("DATABASE_url")

    if not raw_url:
        # Safe fallback for local development if .env is missing
        return "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"

    # Clean whitespace and surrounding quotation marks
    raw_url = raw_url.strip().strip("'").strip('"')

    # Convert protocol to asyncpg driver dialect
    if raw_url.startswith("postgres://"):
        raw_url = "postgresql+asyncpg://" + raw_url[len("postgres://"):]
    elif raw_url.startswith("postgresql://"):
        raw_url = "postgresql+asyncpg://" + raw_url[len("postgresql://"):]

    # Parse URL components and sanitize query parameters for asyncpg
    parsed = urlparse(raw_url)
    query_params = parse_qs(parsed.query)

    # Convert `sslmode=require` -> `ssl=require` for asyncpg compatibility
    if "sslmode" in query_params:
        ssl_val = query_params.pop("sslmode")[0]
        if ssl_val in ("require", "verify-full", "verify-ca"):
            query_params["ssl"] = ["require"]

    # Reassemble sanitized URL
    clean_query = urlencode(query_params, doseq=True)
    clean_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        clean_query,
        parsed.fragment
    ))

    return clean_url


DATABASE_URL = get_normalized_database_url()  


# ==============================================================================
# CONNECTION POOL & ASYNC ENGINE CONFIGURATION
# ==============================================================================
# In production, opening a new TCP socket + SSL handshake to PostgreSQL for EVERY
# request takes 50ms-150ms!
# A connection pool keeps a pool of warm, authenticated connections ready in memory.
engine = create_async_engine(
    DATABASE_URL,
    echo=False,               # Set True if you want to print raw SQL statements in console
    pool_size=10,             # Keep 10 persistent TCP connections open in pool
    max_overflow=20,          # Allow up to 20 extra temporary connections during traffic bursts
    pool_timeout=30,          # Wait maximum 30 seconds for an available connection before raising TimeoutError
    pool_pre_ping=True,       # Crucial for Cloud DBs (Neon/Supabase): Pings DB before handing connection.
                              # If the cloud provider closed an idle socket, it automatically reconnects!
    pool_recycle=300,         # Recycles connections every 5 minutes to prevent stale TCP sockets.
)


# ==============================================================================
# ASYNC SESSION FACTORY
# ==============================================================================
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,   # Allows reading model attributes after `await session.commit()`
    autoflush=False,          # Prevents unexpected automatic flushes before explicit queries
)


# ==============================================================================
# BASE DECLARATIVE CLASS
# ==============================================================================
class Base(DeclarativeBase):
    """Base class for all SQLAlchemy 2.0 mapped models."""
    pass


# ==============================================================================
# FASTAPI ASYNC DATABASE DEPENDENCY (`get_db`)
# ==============================================================================
async def get_db():
    """
    Session-per-request pattern:
    1. Opens an AsyncSession from the connection pool.
    2. Yields the session to the FastAPI path operation function.
    3. If an unhandled exception occurs, rolls back the transaction.
    4. Finally, returns the connection back to the pool cleanly.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


