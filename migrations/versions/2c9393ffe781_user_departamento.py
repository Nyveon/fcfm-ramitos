"""User departamento

Revision ID: 2c9393ffe781
Revises: 8899ce91037b
Create Date: 2024-02-22 21:16:53.842118

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c9393ffe781'
down_revision = '8899ce91037b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('departamento_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_user_departamento', 'departamento', ['departamento_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('fk_user_departamento', type_='foreignkey')
        batch_op.drop_column('departamento_id')

    # ### end Alembic commands ###