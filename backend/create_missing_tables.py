"""Create missing database tables (sessions, tasks, accounts)"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
database_url = os.getenv("DATABASE_URL")

conn = psycopg2.connect(database_url)
cur = conn.cursor()

try:
    # Create sessions table
    print("[INFO] Creating sessions table...")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id UUID PRIMARY KEY,
            user_id UUID NOT NULL,
            token VARCHAR(500) NOT NULL UNIQUE,
            expires_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            ip_address VARCHAR(45),
            user_agent VARCHAR(500),
            created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            CONSTRAINT fk_sessions_user_id FOREIGN KEY (user_id)
                REFERENCES users(id) ON DELETE CASCADE
        );
    """)

    cur.execute("CREATE INDEX IF NOT EXISTS ix_sessions_user_id ON sessions(user_id);")
    cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS ix_sessions_token ON sessions(token);")
    cur.execute("CREATE INDEX IF NOT EXISTS ix_sessions_expires_at ON sessions(expires_at);")

    # Create tasks table
    print("[INFO] Creating tasks table...")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id UUID PRIMARY KEY,
            user_id UUID NOT NULL,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            completed BOOLEAN NOT NULL DEFAULT false,
            priority VARCHAR(10),
            tags VARCHAR[],
            category VARCHAR(50),
            created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            CONSTRAINT fk_tasks_user_id FOREIGN KEY (user_id)
                REFERENCES users(id) ON DELETE CASCADE
        );
    """)

    cur.execute("CREATE INDEX IF NOT EXISTS ix_tasks_user_id ON tasks(user_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS ix_tasks_completed ON tasks(completed);")
    cur.execute("CREATE INDEX IF NOT EXISTS ix_tasks_created_at ON tasks(created_at);")

    # Create accounts table
    print("[INFO] Creating accounts table...")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id UUID PRIMARY KEY,
            user_id UUID NOT NULL,
            provider VARCHAR(50) NOT NULL,
            provider_account_id VARCHAR(255) NOT NULL,
            access_token VARCHAR(500),
            refresh_token VARCHAR(500),
            expires_at TIMESTAMP WITHOUT TIME ZONE,
            created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            CONSTRAINT fk_accounts_user_id FOREIGN KEY (user_id)
                REFERENCES users(id) ON DELETE CASCADE
        );
    """)

    cur.execute("CREATE INDEX IF NOT EXISTS ix_accounts_user_id ON accounts(user_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS ix_accounts_provider ON accounts(provider);")

    conn.commit()
    print("[SUCCESS] All missing tables created successfully")

except Exception as e:
    print(f"[ERROR] {e}")
    conn.rollback()

finally:
    cur.close()
    conn.close()
