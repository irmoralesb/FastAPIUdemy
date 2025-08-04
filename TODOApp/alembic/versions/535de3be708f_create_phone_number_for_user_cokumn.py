"""Create phone number for user cokumn

Revision ID: 535de3be708f
Revises: 
Create Date: 2025-08-03 21:19:39.260583

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '535de3be708f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(),nullable=True))


def downgrade() -> None:
    op.drop_column('users','phone_number')
