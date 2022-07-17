"""Change ruser role structure

Revision ID: 3ae5608e4659
Revises: b4d13ba7e28e
Create Date: 2022-04-24 22:45:27.736179

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3ae5608e4659'
down_revision = 'b4d13ba7e28e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'permissions', ['id'])
    op.create_unique_constraint(None, 'roles', ['id'])
    op.create_unique_constraint(None, 'roles_permissions', ['id'])
    op.create_unique_constraint(None, 'sessions', ['id'])
    op.add_column('user_role', sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False))
    op.add_column('user_role', sa.Column('created', sa.DateTime(), nullable=True))
    op.add_column('user_role', sa.Column('updated', sa.DateTime(), nullable=True))
    op.create_unique_constraint(None, 'user_role', ['id'])
    op.create_unique_constraint(None, 'users', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'user_role', type_='unique')
    op.drop_column('user_role', 'updated')
    op.drop_column('user_role', 'created')
    op.drop_column('user_role', 'id')
    op.drop_constraint(None, 'sessions', type_='unique')
    op.drop_constraint(None, 'roles_permissions', type_='unique')
    op.drop_constraint(None, 'roles', type_='unique')
    op.drop_constraint(None, 'permissions', type_='unique')
    # ### end Alembic commands ###
