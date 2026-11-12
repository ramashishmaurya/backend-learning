"""
================================================================================
DATABASE SEEDING SCRIPT FOR POSTGRESQL ('design' database)
================================================================================
Populates rich, realistic dummy data into:
1. `users`    (12 users)
2. `products` (25 products across Electronics, Books, Furniture, Clothing, Fitness)
3. `orders`   (20 orders with varied statuses and amounts)

Usage:
    python -m api_mastery.seed_data
or
    python api_mastery/seed_data.py
================================================================================
"""

import asyncio
from datetime import datetime, timezone, timedelta
from sqlalchemy import select, delete
from api_mastery.database import engine, Base, AsyncSessionLocal
from api_mastery.models import UserModel, ProductModel, OrderModel

# ------------------------------------------------------------------------------
# 1. DUMMY DATA DEFINITIONS
# ------------------------------------------------------------------------------
DUMMY_USERS = [
    {
        "name": "Rahul Sharma",
        "email": "rahul.sharma@example.com",
        "age": 28,
        "hashed_password": "pbkdf2_sha256$hashed_password_rahul_123",
        "is_active": True,
    },
    {
        "name": "Priya Patel",
        "email": "priya.patel@example.com",
        "age": 25,
        "hashed_password": "pbkdf2_sha256$hashed_password_priya_456",
        "is_active": True,
    },
    {
        "name": "Amit Verma",
        "email": "amit.verma@example.com",
        "age": 34,
        "hashed_password": "pbkdf2_sha256$hashed_password_amit_789",
        "is_active": True,
    },
    {
        "name": "Neha Singh",
        "email": "neha.singh@example.com",
        "age": 22,
        "hashed_password": "pbkdf2_sha256$hashed_password_neha_321",
        "is_active": True,
    },
    {
        "name": "Rajesh Kumar",
        "email": "rajesh.kumar@example.com",
        "age": 42,
        "hashed_password": "pbkdf2_sha256$hashed_password_rajesh_654",
        "is_active": True,
    },
    {
        "name": "Sneha Reddy",
        "email": "sneha.reddy@example.com",
        "age": 29,
        "hashed_password": "pbkdf2_sha256$hashed_password_sneha_987",
        "is_active": False,  # Inactive user for testing filters
    },
    {
        "name": "Vikram Malhotra",
        "email": "vikram.malhotra@example.com",
        "age": 31,
        "hashed_password": "pbkdf2_sha256$hashed_password_vikram_111",
        "is_active": True,
    },
    {
        "name": "Ananya Das",
        "email": "ananya.das@example.com",
        "age": 26,
        "hashed_password": "pbkdf2_sha256$hashed_password_ananya_222",
        "is_active": True,
    },
    {
        "name": "Rohit Joshi",
        "email": "rohit.joshi@example.com",
        "age": 38,
        "hashed_password": "pbkdf2_sha256$hashed_password_rohit_333",
        "is_active": True,
    },
    {
        "name": "Pooja Gupta",
        "email": "pooja.gupta@example.com",
        "age": 24,
        "hashed_password": "pbkdf2_sha256$hashed_password_pooja_444",
        "is_active": True,
    },
    {
        "name": "Karan Mehta",
        "email": "karan.mehta@example.com",
        "age": 45,
        "hashed_password": "pbkdf2_sha256$hashed_password_karan_555",
        "is_active": False,  # Inactive
    },
    {
        "name": "Divya Nair",
        "email": "divya.nair@example.com",
        "age": 27,
        "hashed_password": "pbkdf2_sha256$hashed_password_divya_666",
        "is_active": True,
    },
]

DUMMY_PRODUCTS = [
    # --- ELECTRONICS ---
    {
        "sku": "ELEC-1001",
        "title": "Sony WH-1000XM5 Wireless Noise Cancelling Headphones",
        "description": "Industry leading active noise cancellation with 30-hour battery life and multi-device pairing.",
        "category": "Electronics",
        "price": 26990.0,
        "stock": 45,
        "is_active": True,
    },
    {
        "sku": "ELEC-1002",
        "title": "Keychron K2 Wireless Mechanical Keyboard",
        "description": "75% compact layout with hot-swappable Gateron G Pro Brown switches and RGB backlighting.",
        "category": "Electronics",
        "price": 7999.0,
        "stock": 30,
        "is_active": True,
    },
    {
        "sku": "ELEC-1003",
        "title": "LG 27-inch 4K UHD IPS Monitor (27UP850)",
        "description": "VESA DisplayHDR 400 with USB Type-C 96W power delivery and color-calibrated display.",
        "category": "Electronics",
        "price": 32500.0,
        "stock": 18,
        "is_active": True,
    },
    {
        "sku": "ELEC-1004",
        "title": "Logitech MX Master 3S Ergonomic Mouse",
        "description": "Quiet clicks, 8K DPI any-surface tracking, and ultra-fast MagSpeed electromagnetic scrolling.",
        "category": "Electronics",
        "price": 8495.0,
        "stock": 50,
        "is_active": True,
    },
    {
        "sku": "ELEC-1005",
        "title": "Anker 65W GaN Fast Charger 3-Port",
        "description": "Compact foldable wall charger supporting Power Delivery (PD) for laptops, tablets, and phones.",
        "category": "Electronics",
        "price": 2999.0,
        "stock": 100,
        "is_active": True,
    },
    {
        "sku": "ELEC-1006",
        "title": "Apple Watch Series 9 GPS 45mm",
        "description": "Always-On Retina display with S9 SiP chip, double tap gesture, and blood oxygen tracking.",
        "category": "Electronics",
        "price": 44900.0,
        "stock": 12,
        "is_active": True,
    },
    {
        "sku": "ELEC-1007",
        "title": "JBL Flip 6 Portable Bluetooth Speaker",
        "description": "IP67 waterproof and dustproof with 2-way speaker system and 12-hour playtime.",
        "category": "Electronics",
        "price": 8999.0,
        "stock": 35,
        "is_active": True,
    },
    {
        "sku": "ELEC-1008",
        "title": "Logitech C920 Pro HD 1080p Webcam",
        "description": "Full HD 1080p video calling with stereo audio and automatic light correction.",
        "category": "Electronics",
        "price": 5495.0,
        "stock": 0,  # Out of stock for testing
        "is_active": True,
    },

    # --- BOOKS ---
    {
        "sku": "BOOK-2001",
        "title": "Designing Data-Intensive Applications",
        "description": "The definitive guide to distributed databases, reliable architecture, and consensus by Martin Kleppmann.",
        "category": "Books",
        "price": 1850.0,
        "stock": 80,
        "is_active": True,
    },
    {
        "sku": "BOOK-2002",
        "title": "Clean Code: Agile Software Craftsmanship",
        "description": "Handbook of agile software craft, refactoring patterns, and maintainable code by Robert C. Martin.",
        "category": "Books",
        "price": 899.0,
        "stock": 65,
        "is_active": True,
    },
    {
        "sku": "BOOK-2003",
        "title": "System Design Interview (Volume 1 & 2)",
        "description": "Step-by-step insider guide to scaling backend architectures and acing system design interviews by Alex Xu.",
        "category": "Books",
        "price": 2400.0,
        "stock": 40,
        "is_active": True,
    },
    {
        "sku": "BOOK-2004",
        "title": "Fluent Python: Clear, Concise, and Effective Programming",
        "description": "Master idiomatic Python 3, decorators, concurrency, asyncio, and type hints by Luciano Ramalho.",
        "category": "Books",
        "price": 2150.0,
        "stock": 25,
        "is_active": True,
    },
    {
        "sku": "BOOK-2005",
        "title": "The Pragmatic Programmer (20th Anniversary Edition)",
        "description": "Your journey to software mastery, responsibility, and continuous technical growth by David Thomas & Andrew Hunt.",
        "category": "Books",
        "price": 1499.0,
        "stock": 50,
        "is_active": True,
    },
    {
        "sku": "BOOK-2006",
        "title": "Grokking Algorithms: An Illustrated Guide",
        "description": "A friendly, visual guide that teaches fundamental sorting, graph, and dynamic programming algorithms by Aditya Bhargava.",
        "category": "Books",
        "price": 750.0,
        "stock": 90,
        "is_active": True,
    },

    # --- FURNITURE ---
    {
        "sku": "FURN-3001",
        "title": "Green Soul Ergonomic High-Back Mesh Chair",
        "description": "Breathable mesh backrest, adjustable 3D armrests, dynamic lumbar support, and heavy-duty nylon base.",
        "category": "Furniture",
        "price": 12999.0,
        "stock": 20,
        "is_active": True,
    },
    {
        "sku": "FURN-3002",
        "title": "Dual-Motor Electric Standing Desk (140x70cm)",
        "description": "Seamless motorized height adjustment (70cm - 120cm) with 4 memory presets and cable organizer.",
        "category": "Furniture",
        "price": 24500.0,
        "stock": 15,
        "is_active": True,
    },
    {
        "sku": "FURN-3003",
        "title": "Solid Oak Monitor Riser Stand with Drawer",
        "description": "Ergonomic wooden desktop monitor riser with slide-out storage drawer and phone holder slot.",
        "category": "Furniture",
        "price": 2499.0,
        "stock": 40,
        "is_active": True,
    },
    {
        "sku": "FURN-3004",
        "title": "Ergonomic Memory Foam Under-Desk Footrest",
        "description": "High-density teardrop shaped foot cushion for improved posture, blood circulation, and sciatica relief.",
        "category": "Furniture",
        "price": 1299.0,
        "stock": 60,
        "is_active": True,
    },

    # --- CLOTHING ---
    {
        "sku": "CLOTH-4001",
        "title": "100% Pima Cotton Heavyweight Crewneck T-Shirt",
        "description": "Pre-shrunk 240 GSM luxury cotton t-shirt with ribbed collar and tailored regular fit.",
        "category": "Clothing",
        "price": 999.0,
        "stock": 120,
        "is_active": True,
    },
    {
        "sku": "CLOTH-4002",
        "title": "Levi's 511 Slim Fit Stretch Denim Jeans",
        "description": "Modern slim cut with room to move, premium denim washed with water-saving techniques.",
        "category": "Clothing",
        "price": 3199.0,
        "stock": 45,
        "is_active": True,
    },
    {
        "sku": "CLOTH-4003",
        "title": "Columbia Waterproof Hooded Windbreaker",
        "description": "Omni-Tech waterproof breathable seam-sealed shell jacket with packable pocket design.",
        "category": "Clothing",
        "price": 5499.0,
        "stock": 22,
        "is_active": True,
    },
    {
        "sku": "CLOTH-4004",
        "title": "Nike Air Zoom Pegasus 40 Running Shoes",
        "description": "Responsive road running shoes with React foam cushioning and engineered mesh upper.",
        "category": "Clothing",
        "price": 9695.0,
        "stock": 30,
        "is_active": True,
    },

    # --- FITNESS ---
    {
        "sku": "FIT-5001",
        "title": "Kore 20kg Adjustable Rubber Dumbbell Set",
        "description": "Complete home gym combo including cast-iron plates, chrome spinlock collars, and non-slip knurled handles.",
        "category": "Fitness",
        "price": 1899.0,
        "stock": 55,
        "is_active": True,
    },
    {
        "sku": "FIT-5002",
        "title": "Boldfit 6mm Eco-Friendly Anti-Tear Yoga Mat",
        "description": "Non-slip dual-sided textured surface with body alignment lines and carry strap.",
        "category": "Fitness",
        "price": 1199.0,
        "stock": 70,
        "is_active": True,
    },
    {
        "sku": "FIT-5003",
        "title": "Heavy-Duty Resistance Loop Bands (Set of 5)",
        "description": "100% natural latex resistance bands for strength training, physical therapy, and warm-ups.",
        "category": "Fitness",
        "price": 649.0,
        "stock": 110,
        "is_active": True,
    },
    {
        "sku": "FIT-5004",
        "title": "BlenderBottle Strada Insulated Shaker (700ml)",
        "description": "Double-wall vacuum insulated stainless steel shaker cup with push-button flip cap and wire whisk.",
        "category": "Fitness",
        "price": 1999.0,
        "stock": 0,  # Out of stock
        "is_active": False,  # Archived product for testing inactive filters
    },
]


async def seed_database():
    """
    Connects to the PostgreSQL database, ensures tables exist,
    and inserts dummy users, products, and orders.
    """
    print("\n" + "=" * 70)
    print(">>> [POSTGRESQL SEEDER] Initializing database seeding for 'design' DB...")
    print("=" * 70)

    # 1. Create tables if they do not exist
    async with engine.begin() as conn:
        print(">>> Creating / verifying tables (users, products, orders)...")
        await conn.run_sync(Base.metadata.create_all)
        print(">>> Tables are verified and ready!")

    # 2. Insert Data
    async with AsyncSessionLocal() as session:
        # Check existing counts
        user_count_result = await session.execute(select(UserModel.id))
        existing_user_count = len(user_count_result.scalars().all())

        product_count_result = await session.execute(select(ProductModel.id))
        existing_product_count = len(product_count_result.scalars().all())

        order_count_result = await session.execute(select(OrderModel.id))
        existing_order_count = len(order_count_result.scalars().all())

        print(f"\n[INFO] Current Records in DB: {existing_user_count} Users | {existing_product_count} Products | {existing_order_count} Orders")

        # Clean slate or append? We will upsert / populate if empty or refresh
        if existing_user_count > 0 or existing_product_count > 0:
            print(">>> Existing records detected. Resetting tables to ensure clean, non-conflicting dummy data...")
            # Delete in order of dependencies (orders first due to FK, then users, products)
            await session.execute(delete(OrderModel))
            await session.execute(delete(UserModel))
            await session.execute(delete(ProductModel))
            await session.commit()
            print(">>> Cleaned previous records successfully.")

        # --- SEED USERS ---
        print("\n>>> Seeding Users...")
        created_users = []
        now = datetime.now(timezone.utc)
        for i, u_data in enumerate(DUMMY_USERS):
            user = UserModel(
                name=u_data["name"],
                email=u_data["email"],
                age=u_data["age"],
                hashed_password=u_data["hashed_password"],
                is_active=u_data["is_active"],
                created_at=now - timedelta(days=len(DUMMY_USERS) - i)
            )
            session.add(user)
            created_users.append(user)

        await session.commit()
        # Refresh to get autogenerated IDs
        for u in created_users:
            await session.refresh(u)
        print(f"[SUCCESS] Successfully seeded {len(created_users)} Users!")

        # --- SEED PRODUCTS ---
        print("\n>>> Seeding Products...")
        created_products = []
        for i, p_data in enumerate(DUMMY_PRODUCTS):
            product = ProductModel(
                sku=p_data["sku"],
                title=p_data["title"],
                description=p_data["description"],
                category=p_data["category"],
                price=p_data["price"],
                stock=p_data["stock"],
                is_active=p_data["is_active"],
                created_at=now - timedelta(days=len(DUMMY_PRODUCTS) - i)
            )
            session.add(product)
            created_products.append(product)

        await session.commit()
        for p in created_products:
            await session.refresh(p)
        print(f"[SUCCESS] Successfully seeded {len(created_products)} Products across 5 categories!")

        # --- SEED ORDERS ---
        print("\n>>> Seeding Orders linked to Users...")
        order_templates = [
            (0, 26990.0, "DELIVERED", 20),
            (0, 1850.0, "DELIVERED", 15),
            (1, 7999.0, "SHIPPED", 5),
            (1, 899.0, "PAID", 2),
            (2, 32500.0, "DELIVERED", 18),
            (2, 24500.0, "PENDING", 1),
            (3, 8495.0, "PAID", 3),
            (3, 999.0, "DELIVERED", 10),
            (4, 2999.0, "DELIVERED", 12),
            (4, 2400.0, "SHIPPED", 4),
            (6, 44900.0, "PAID", 2),
            (6, 12999.0, "DELIVERED", 14),
            (7, 8999.0, "DELIVERED", 8),
            (7, 2150.0, "SHIPPED", 3),
            (8, 1899.0, "DELIVERED", 11),
            (8, 1499.0, "CANCELLED", 7),
            (9, 1199.0, "PAID", 1),
            (9, 750.0, "DELIVERED", 6),
            (11, 649.0, "DELIVERED", 9),
            (11, 3199.0, "PENDING", 0),
        ]

        created_orders = []
        for user_idx, amount, status_val, days_ago in order_templates:
            user_obj = created_users[user_idx % len(created_users)]
            order = OrderModel(
                user_id=user_obj.id,
                total_amount=amount,
                status=status_val,
                created_at=now - timedelta(days=days_ago)
            )
            session.add(order)
            created_orders.append(order)

        await session.commit()
        print(f"[SUCCESS] Successfully seeded {len(created_orders)} Orders!")

    print("\n" + "=" * 70)
    print("[SUCCESS] SEEDING COMPLETED SUCCESSFULLY IN POSTGRESQL ('design' DB)!")
    print(f"   - Users Table:    {len(created_users)} rows")
    print(f"   - Products Table: {len(created_products)} rows")
    print(f"   - Orders Table:   {len(created_orders)} rows")
    print("=" * 70 + "\n")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_database())
