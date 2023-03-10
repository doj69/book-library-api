"""alter book table

Revision ID: 2dfda461ea63
Revises: d98b376d5a5c
Create Date: 2022-12-26 22:59:27.139199

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2dfda461ea63'
down_revision = 'd98b376d5a5c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('is_available', sa.Boolean(), nullable=True))
    op.drop_column('borrowed_books', 'status')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('borrowed_books', sa.Column('status', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_column('books', 'is_available')
    # ### end Alembic commands ###
