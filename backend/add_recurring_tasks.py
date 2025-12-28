"""
Database Migration: Add Recurring Task Support
Adds is_recurring, recurrence_pattern, and parent_task_id columns to tasks table
Author: Sharmeen Asif
"""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def add_recurring_columns():
    """Add recurring task columns to tasks table."""
    engine = create_async_engine(DATABASE_URL, echo=True)

    try:
        async with engine.begin() as conn:
            print("Adding recurring task columns...")

            # Add is_recurring column
            await conn.execute(text("""
                ALTER TABLE tasks
                ADD COLUMN IF NOT EXISTS is_recurring BOOLEAN DEFAULT FALSE NOT NULL
            """))
            print("[OK] Added is_recurring column")

            # Add recurrence_pattern column
            await conn.execute(text("""
                ALTER TABLE tasks
                ADD COLUMN IF NOT EXISTS recurrence_pattern VARCHAR(20)
            """))
            print("[OK] Added recurrence_pattern column")

            # Add parent_task_id column
            await conn.execute(text("""
                ALTER TABLE tasks
                ADD COLUMN IF NOT EXISTS parent_task_id UUID REFERENCES tasks(id)
            """))
            print("[OK] Added parent_task_id column")

            print("\n[SUCCESS] All recurring task columns added successfully!")

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(add_recurring_columns())
