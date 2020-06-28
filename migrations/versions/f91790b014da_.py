"""empty message

Revision ID: f91790b014da
Revises: 8ed254c0debb
Create Date: 2020-06-28 17:08:43.802877

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f91790b014da'
down_revision = '8ed254c0debb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('website_link', sa.String(), nullable=True))
    op.drop_column('artists', 'website')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('website', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('artists', 'website_link')
    # ### end Alembic commands ###
