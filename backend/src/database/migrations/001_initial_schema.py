"""
Initial database schema migration for the Todo application.
This migration creates the users and todos tables with all necessary fields and indexes.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    """
    Create the initial database schema for users and todos tables.
    """
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Create todos table
    op.create_table(
        'todos',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, default=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )

    # Create indexes for performance
    op.create_index('idx_users_email', 'users', ['email'])
    op.create_index('idx_users_created_at', 'users', ['created_at'])
    op.create_index('idx_todos_user_id', 'todos', ['user_id'])
    op.create_index('idx_todos_completed', 'todos', ['completed'])
    op.create_index('idx_todos_created_at', 'todos', ['created_at'])
    op.create_index('idx_todos_updated_at', 'todos', ['updated_at'])
    op.create_index('idx_todos_user_id_completed', 'todos', ['user_id', 'completed'])


def downgrade():
    """
    Drop the database schema created in the upgrade function.
    NOTE: This will permanently delete all data in the tables.
    """
    # Drop indexes
    op.drop_index('idx_todos_user_id_completed', table_name='todos')
    op.drop_index('idx_todos_updated_at', table_name='todos')
    op.drop_index('idx_todos_created_at', table_name='todos')
    op.drop_index('idx_todos_completed', table_name='todos')
    op.drop_index('idx_todos_user_id', table_name='todos')
    op.drop_index('idx_users_created_at', table_name='users')
    op.drop_index('idx_users_email', table_name='users')

    # Drop tables
    op.drop_table('todos')
    op.drop_table('users')