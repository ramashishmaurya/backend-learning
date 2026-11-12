"""
================================================================================
STANDALONE DATABASE CONNECTION & OPERATIONS RUNNER
================================================================================
Run this file directly to test live connection to PostgreSQL ('design' database)
and perform real database operations!

Usage:
    python backend/connect.py
================================================================================
"""

import asyncio
import sys
from pathlib import Path

# Ensure root directory is on Python path for standalone script execution
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select, func, text
from backend.database import engine, AsyncSessionLocal
from backend.models import UserModel, ProductModel, OrderModel


async def main():
    print("=" * 65)
    print(">>> Connecting to PostgreSQL Database: 'design'...")
    print("=" * 65)

    # 1. Test ping
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT current_database(), version();"))
            db_name, version = result.fetchone()
            print(f"[SUCCESS] Connected successfully to database: '{db_name}'")
            print(f"[INFO] Engine Version: {version[:45]}...")
    except Exception as e:
        print(f"[ERROR] Could not connect to database: {e}")
        return

    # 2. Perform Real Database Operations using AsyncSession
    async with AsyncSessionLocal() as session:
        # A. Count Total Records in Existing Tables
        user_count = (await session.execute(select(func.count(UserModel.id)))).scalar_one()
        product_count = (await session.execute(select(func.count(ProductModel.id)))).scalar_one()
        order_count = (await session.execute(select(func.count(OrderModel.id)))).scalar_one()

        print("\n--- DATABASE SUMMARY ---")
        print(f"Total Users in DB:    {user_count}")
        print(f"Total Products in DB: {product_count}")
        print(f"Total Orders in DB:   {order_count}")

        # B. Operation 1: Fetch Top 5 Products by Price (Highest first)
        print("\n--- OPERATION 1: TOP 5 HIGHEST PRICE PRODUCTS ---")
        query_top_products = (
            select(ProductModel)
            .order_by(ProductModel.price.desc())
            .limit(5)
        )
        top_products = (await session.execute(query_top_products)).scalars().all()
        for idx, prod in enumerate(top_products, 1):
            print(f"  {idx}. [{prod.sku}] {prod.title[:40]:<40} | Rs.{prod.price:>9.2f} | Stock: {prod.stock}")

        # C. Operation 2: Fetch Recent 3 Users with their Order Count
        print("\n--- OPERATION 2: RECENT USERS ---")
        query_users = select(UserModel).order_by(UserModel.id.desc()).limit(3)
        users = (await session.execute(query_users)).scalars().all()
        for u in users:
            print(f"  - User ID: {u.id} | Name: {u.name:<15} | Email: {u.email:<25} | Orders: {len(u.orders)}")

        # D. Operation 3: Filter Products by Category (e.g. 'Books')
        print("\n--- OPERATION 3: FILTER BY CATEGORY ('Books') ---")
        query_books = select(ProductModel).where(ProductModel.category == "Books").limit(3)
        books = (await session.execute(query_books)).scalars().all()
        for b in books:
            print(f"  - Book: {b.title:<45} | Rs.{b.price}")

    print("\n" + "=" * 65)
    print("[SUCCESS] All operations on actual PostgreSQL database completed successfully!")
    print("=" * 65)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
