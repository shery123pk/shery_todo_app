"""Initial schema

Revision ID: 001_initial_schema
Revises:
Create Date: 2025-12-26 00:00:00.000000

Creates all 4 core tables:
- users: User authentication and profiles
- tasks: Todo items with user ownership
- sessions: Authentication sessions
- accounts: OAuth provider accounts

All tables use UUID primary keys.
Tasks and sessions have CASCADE delete on user_id foreign key.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects.postgresql import UUID, ARRAY


# revision identifiers, used by Alembic.
revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create all tables and indexes"""

    # Create users table
    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('email_verified', sa.Boolean(), nullable=False, default=False),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # Create indexes on users table
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, default=False),
        sa.Column('priority', sa.String(length=10), nullable=True),
        sa.Column('tags', ARRAY(sa.String()), nullable=True, default=[]),
        sa.Column('category', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )

    # Create indexes on tasks table
    op.create_index('ix_tasks_user_id', 'tasks', ['user_id'])
    op.create_index('ix_tasks_completed', 'tasks', ['completed'])
    op.create_index('ix_tasks_created_at', 'tasks', ['created_at'])

    # Create composite index for main query (user_id, completed, created_at DESC)
    op.create_index(
        'ix_tasks_user_completed_created',
        'tasks',
        ['user_id', 'completed', sa.text('created_at DESC')]
    )

    # Create sessions table
    op.create_table(
        'sessions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), nullable=False),
        sa.Column('token', sa.String(length=500), nullable=False, unique=True),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )

    # Create indexes on sessions table
    op.create_index('ix_sessions_user_id', 'sessions', ['user_id'])
    op.create_index('ix_sessions_token', 'sessions', ['token'], unique=True)
    op.create_index('ix_sessions_expires_at', 'sessions', ['expires_at'])

    # Create accounts table (for OAuth)
    op.create_table(
        'accounts',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), nullable=False),
        sa.Column('provider', sa.String(length=50), nullable=False),
        sa.Column('provider_account_id', sa.String(length=255), nullable=False),
        sa.Column('access_token', sa.String(length=500), nullable=True),
        sa.Column('refresh_token', sa.String(length=500), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )

    # Create indexes on accounts table
    op.create_index('ix_accounts_user_id', 'accounts', ['user_id'])
    op.create_index('ix_accounts_provider', 'accounts', ['provider'])


def downgrade() -> None:
    """Drop all tables"""
    op.drop_table('accounts')
    op.drop_table('sessions')
    op.drop_table('tasks')
    op.drop_table('users')
