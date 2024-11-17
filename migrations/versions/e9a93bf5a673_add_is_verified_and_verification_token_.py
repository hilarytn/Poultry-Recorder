"""Add is_verified and verification_token to User model

Revision ID: e9a93bf5a673
Revises: f4181210610d
Create Date: 2024-11-01 07:43:53.052933

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9a93bf5a673'
down_revision = 'f4181210610d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_verified', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('verification_token', sa.String(length=128), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('verification_token')
        batch_op.drop_column('is_verified')

    # ### end Alembic commands ###