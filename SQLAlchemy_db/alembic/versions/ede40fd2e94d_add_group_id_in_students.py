"""add group_id in students

Revision ID: ede40fd2e94d
Revises: 53431c0d4fbd
Create Date: 2023-09-03 21:01:51.142977

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ede40fd2e94d"
down_revision: Union[str, None] = "53431c0d4fbd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("students", sa.Column("group_id", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "students", "groups", ["group_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "students", type_="foreignkey")
    op.drop_column("students", "group_id")
    # ### end Alembic commands ###
