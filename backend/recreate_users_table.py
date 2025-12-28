"""
Drop and recreate users table with correct schema
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
    print("[INFO] Dropping old users table...")
    cur.execute("DROP TABLE IF EXISTS users CASCADE;")

    print("[INFO] Creating new users table...")
    cur.execute("""
        CREATE TABLE users (
            id UUID PRIMARY KEY,
            email VARCHAR(255) NOT NULL UNIQUE,
            email_verified BOOLEAN NOT NULL DEFAULT false,
            name VARCHAR(255),
            hashed_password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL
        );
    """)

    print("[INFO] Creating index on email...")
    cur.execute("CREATE INDEX ix_users_email ON users(email);")

    conn.commit()
    print("[SUCCESS] Users table recreated successfully")
    print("[INFO] You can now sign up with a new account")

except Exception as e:
    conn.rollback()
    print(f"[ERROR] {e}")

finally:
    cur.close()
    conn.close()
