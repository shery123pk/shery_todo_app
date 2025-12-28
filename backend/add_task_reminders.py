"""
Database Migration: Add Task Reminder Fields
Adds due_date and reminder_sent columns to tasks table
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

async def add_reminder_fields():
    """Add due_date and reminder_sent columns to tasks table."""
    engine = create_async_engine(DATABASE_URL, echo=True)

    try:
        async with engine.begin() as conn:
            print("Adding due_date and reminder_sent columns...")

            # Add due_date column
            await conn.execute(text("""
                ALTER TABLE tasks
                ADD COLUMN IF NOT EXISTS due_date TIMESTAMP
            """))
            print("[OK] Added due_date column")

            # Add reminder_sent column
            await conn.execute(text("""
                ALTER TABLE tasks
                ADD COLUMN IF NOT EXISTS reminder_sent BOOLEAN DEFAULT FALSE NOT NULL
            """))
            print("[OK] Added reminder_sent column")

            # Create index on due_date for faster queries
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS ix_tasks_due_date ON tasks (due_date)
            """))
            print("[OK] Created index on due_date")

            print("\n[SUCCESS] All reminder fields added successfully!")

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    print("Running migration: Add task reminder fields")
    asyncio.run(add_reminder_fields())
    print("Migration complete!")
