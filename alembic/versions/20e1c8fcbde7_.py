"""empty message

Revision ID: 20e1c8fcbde7
Revises: e786d4650f75
Create Date: 2024-05-17 20:17:05.145147

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20e1c8fcbde7"
down_revision: Union[str, None] = "e786d4650f75"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("subjects", sa.Column("credits", sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("subjects", "credits")
    # ### end Alembic commands ###