"""Actor table

Revision ID: 3cc1a1982fb1
Revises: fbaf9a2c88dd
Create Date: 2018-09-18 20:05:32.919465

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3cc1a1982fb1'
down_revision = 'fbaf9a2c88dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('actor', sa.Column('photo', sa.String(length=120), nullable=True))
    op.add_column('movie', sa.Column('photo', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('movie', 'photo')
    op.drop_column('actor', 'photo')
    # ### end Alembic commands ###
