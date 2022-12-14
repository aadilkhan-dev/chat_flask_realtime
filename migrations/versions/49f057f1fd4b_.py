"""empty message

Revision ID: 49f057f1fd4b
Revises: 760b9b7b3d51
Create Date: 2022-10-03 18:50:14.693227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49f057f1fd4b'
down_revision = '760b9b7b3d51'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('conected_user',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('user_name', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('conected_user')
    # ### end Alembic commands ###
