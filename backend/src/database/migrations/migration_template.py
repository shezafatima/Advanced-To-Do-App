"""
Template for creating new database migration scripts.
Copy this file and update the upgrade/downgrade functions as needed.

Migration naming convention: {number}_{short_description}.py
Example: 002_add_user_profile_fields.py
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    """
    Apply the migration changes to upgrade the database schema.
    Add your specific migration logic here.
    """
    # Example: Add a new column
    # op.add_column('users', sa.Column('new_field', sa.String(100), nullable=True))

    # Example: Create a new table
    # op.create_table(
    #     'new_table',
    #     sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    #     sa.Column('name', sa.String(255), nullable=False),
    #     sa.PrimaryKeyConstraint('id')
    # )

    # Example: Create an index
    # op.create_index('idx_new_table_name', 'new_table', ['name'])

    print("Upgrade migration applied successfully")


def downgrade():
    """
    Revert the migration changes to downgrade the database schema.
    Add the reverse logic for your migration here.
    """
    # Example: Drop the column added in upgrade
    # op.drop_column('users', 'new_field')

    # Example: Drop the table created in upgrade
    # op.drop_table('new_table')

    # Example: Drop the index created in upgrade
    # op.drop_index('idx_new_table_name', table_name='new_table')

    print("Downgrade migration applied successfully")