"""Agregando pais a usuarios

Revision ID: 090dc43aa6b2
Revises: ddf432cd1f7a
Create Date: 2022-11-20 12:48:42.975930

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '090dc43aa6b2'
down_revision = 'ddf432cd1f7a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usuario', sa.Column('pais', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usuario', 'pais')
    # ### end Alembic commands ###