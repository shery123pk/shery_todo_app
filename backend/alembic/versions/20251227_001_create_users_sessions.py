"""Update users and sessions for auth system

Revision ID: 20251227_001
Revises: 001_initial_schema
Create Date: 2025-12-27

Adds new fields to users table:
- full_name (required)
- avatar_url, timezone, language (optional)

Adds to sessions table:
- refresh_token field

Updates timestamps to use TIMESTAMPTZ

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '20251227_001'
down_revision = '001_initial_schema'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Update users table
    op.add_column('users', sa.Column('full_name', sa.String(length=255), nullable=True))  # Nullable during migration
    op.add_column('users', sa.Column('avatar_url', sa.String(length=500), nullable=True))
    op.add_column('users', sa.Column('timezone', sa.String(length=50), nullable=True))
    op.add_column('users', sa.Column('language', sa.String(length=10), nullable=True))

    # Set default value for existing users
    op.execute("UPDATE users SET full_name = 'User' WHERE full_name IS NULL")

    # Make full_name NOT NULL
    op.alter_column('users', 'full_name', nullable=False)

    # Rename 'name' column to 'full_name' if it exists (from old schema)
    # op.alter_column('users', 'name', new_column_name='full_name')

    # Update timestamp columns to TIMESTAMPTZ
    op.alter_column('users', 'created_at',
                    type_=sa.TIMESTAMP(timezone=True),
                    existing_type=sa.DateTime(),
                    server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('users', 'updated_at',
                    type_=sa.TIMESTAMP(timezone=True),
                    existing_type=sa.DateTime(),
                    server_default=sa.text('CURRENT_TIMESTAMP'))

    # Update sessions table
    op.add_column('sessions', sa.Column('refresh_token', sa.String(length=500), nullable=True, unique=True))

    # Set a default refresh_token for existing sessions (same as token for migration)
    op.execute("UPDATE sessions SET refresh_token = token WHERE refresh_token IS NULL")

    # Make refresh_token NOT NULL and add unique constraint
    op.alter_column('sessions', 'refresh_token', nullable=False)
    op.create_index('ix_sessions_refresh_token', 'sessions', ['refresh_token'], unique=True)

    # Update session timestamps to TIMESTAMPTZ
    op.alter_column('sessions', 'created_at',
                    type_=sa.TIMESTAMP(timezone=True),
                    existing_type=sa.DateTime(),
                    server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('sessions', 'expires_at',
                    type_=sa.TIMESTAMP(timezone=True),
                    existing_type=sa.DateTime())


def downgrade() -> None:
    # Revert sessions
    op.drop_index('ix_sessions_refresh_token', table_name='sessions')
    op.drop_column('sessions', 'refresh_token')
    op.alter_column('sessions', 'expires_at',
                    type_=sa.DateTime(),
                    existing_type=sa.TIMESTAMP(timezone=True))
    op.alter_column('sessions', 'created_at',
                    type_=sa.DateTime(),
                    existing_type=sa.TIMESTAMP(timezone=True))

    # Revert users
    op.alter_column('users', 'updated_at',
                    type_=sa.DateTime(),
                    existing_type=sa.TIMESTAMP(timezone=True))
    op.alter_column('users', 'created_at',
                    type_=sa.DateTime(),
                    existing_type=sa.TIMESTAMP(timezone=True))
    op.drop_column('users', 'language')
    op.drop_column('users', 'timezone')
    op.drop_column('users', 'avatar_url')
    op.drop_column('users', 'full_name')
