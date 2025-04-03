"""create app_clusters table

Revision ID: 551f45b7dab8
Revises: 95549847d413
Create Date: 2025-04-03 10:54:22.539162
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import uuid
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '551f45b7dab8'
down_revision: Union[str, None] = '95549847d413'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'app_clusters',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('app_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('apps.id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('cluster', sa.Integer(), nullable=False),
        sa.Column('x', sa.Float(), nullable=False),
        sa.Column('y', sa.Float(), nullable=False),
        sa.Column('downloads', sa.Float(), nullable=True),
        sa.Column('revenue', sa.Float(), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('app_clusters')
