"""movies table

Revision ID: f267ad7666ad
Revises: 
Create Date: 2018-09-06 20:11:46.495838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f267ad7666ad'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('actor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('actor_name_en', sa.String(length=64), nullable=True),
    sa.Column('actor_name_kr', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_actor_actor_name_en'), 'actor', ['actor_name_en'], unique=True)
    op.create_index(op.f('ix_actor_actor_name_kr'), 'actor', ['actor_name_kr'], unique=True)
    op.create_table('director',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('director_name_en', sa.String(length=64), nullable=True),
    sa.Column('director_name_kr', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_director_director_name_en'), 'director', ['director_name_en'], unique=True)
    op.create_index(op.f('ix_director_director_name_kr'), 'director', ['director_name_kr'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_director_director_name_kr'), table_name='director')
    op.drop_index(op.f('ix_director_director_name_en'), table_name='director')
    op.drop_table('director')
    op.drop_index(op.f('ix_actor_actor_name_kr'), table_name='actor')
    op.drop_index(op.f('ix_actor_actor_name_en'), table_name='actor')
    op.drop_table('actor')
    # ### end Alembic commands ###
