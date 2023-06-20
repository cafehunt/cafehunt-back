"""merge heads

Revision ID: 91889c8962dc
Revises: dc5be5ab754b, d119af189950
Create Date: 2023-06-20 14:41:40.715202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91889c8962dc'
down_revision = ('dc5be5ab754b', 'd119af189950')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
