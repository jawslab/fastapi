"""empty message

Revision ID: 1eb0ddc8cab6
Revises: aaed6ef30c62
Create Date: 2024-09-17 10:45:17.454635

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1eb0ddc8cab6'
down_revision: Union[str, None] = 'aaed6ef30c62'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
