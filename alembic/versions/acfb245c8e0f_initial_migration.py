"""Initial migration

Revision ID: acfb245c8e0f
Revises: 48db5508e2d2
Create Date: 2024-08-16 06:46:47.695536

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'acfb245c8e0f'
down_revision: Union[str, None] = '48db5508e2d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('scrapeddata',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('meta_description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('headings', sa.Text(), nullable=True),
    sa.Column('links', sa.Text(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('scrapeddata')
    # ### end Alembic commands ###
