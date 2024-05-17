"""current_sum -> ForiegnKey

Revision ID: 612f5a4c37b3
Revises: 294592dae1e8
Create Date: 2024-05-17 07:31:28.427855

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "612f5a4c37b3"
down_revision: Union[str, None] = "294592dae1e8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_students_current_sem", table_name="students")
    op.create_foreign_key(None, "students", "semesters", ["current_sem"], ["sem_id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "students", type_="foreignkey")
    op.create_index(
        "ix_students_current_sem", "students", ["current_sem"], unique=False
    )
    # ### end Alembic commands ###
