"""
Quick script to add missing email_verified column to users table
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Get database URL
database_url = os.getenv("DATABASE_URL")

# Connect to database
conn = psycopg2.connect(database_url)
cur = conn.cursor()

try:
    # Add email_verified column if it doesn't exist
    cur.execute("""
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS email_verified BOOLEAN NOT NULL DEFAULT false;
    """)

    conn.commit()
    print("[SUCCESS] Added email_verified column to users table")

except Exception as e:
    conn.rollback()
    print(f"[ERROR] {e}")

finally:
    cur.close()
    conn.close()
