"""add date to grades

Revision ID: c0033d1ca4fc
Revises: ede40fd2e94d
Create Date: 2023-09-05 22:22:19.086493

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c0033d1ca4fc"
down_revision: Union[str, None] = "ede40fd2e94d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("grades", sa.Column("date", sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("grades", "date")
    # ### end Alembic commands ###