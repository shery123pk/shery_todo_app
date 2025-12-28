"""
Check and fix database schema to match models
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
    # Check what columns exist in users table
    cur.execute("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'users'
        ORDER BY ordinal_position;
    """)

    print("[INFO] Current columns in users table:")
    existing_columns = []
    for row in cur.fetchall():
        print(f"  - {row[0]}: {row[1]}")
        existing_columns.append(row[0])

    # Add missing columns
    columns_to_add = [
        ("email_verified", "BOOLEAN NOT NULL DEFAULT false"),
        ("name", "VARCHAR(255)"),
    ]

    for col_name, col_type in columns_to_add:
        if col_name not in existing_columns:
            print(f"[INFO] Adding column: {col_name}")
            cur.execute(f"""
                ALTER TABLE users
                ADD COLUMN {col_name} {col_type};
            """)
        else:
            print(f"[SKIP] Column {col_name} already exists")

    conn.commit()
    print("[SUCCESS] Schema updated successfully")

except Exception as e:
    conn.rollback()
    print(f"[ERROR] {e}")

finally:
    cur.close()
    conn.close()
