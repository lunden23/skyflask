"""empty message

Revision ID: 859443de4d46
Revises: 
Create Date: 2022-01-27 17:28:48.204302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '859443de4d46'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('registered_on', sa.DateTime(), nullable=False),
    sa.Column('confirmed', sa.Boolean(), nullable=False),
    sa.Column('confirmed_on', sa.DateTime(), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('package',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('version', sa.String(length=30), nullable=False),
    sa.Column('author', sa.String(length=100), nullable=False),
    sa.Column('nsfw', sa.Boolean(), nullable=False),
    sa.Column('summary', sa.String(length=230), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('requirements', sa.Text(), nullable=False),
    sa.Column('package_dir', sa.String(length=400), nullable=False),
    sa.Column('date_uploaded', sa.DateTime(), nullable=False),
    sa.Column('downloads_total', sa.BigInteger(), nullable=False),
    sa.Column('downloads_current_version', sa.BigInteger(), nullable=False),
    sa.Column('likes', sa.BigInteger(), nullable=False),
    sa.Column('views_total', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('package_dir')
    )
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['package.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comment', sa.Text(), nullable=False),
    sa.Column('date_posted', sa.DateTime(), nullable=False),
    sa.Column('user', sa.Integer(), nullable=False),
    sa.Column('package', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['package'], ['package.id'], ),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('package_animations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('version', sa.String(), nullable=False),
    sa.Column('package_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['package_id'], ['package.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('version')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('package_animations')
    op.drop_table('comment')
    op.drop_table('categories')
    op.drop_table('package')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###