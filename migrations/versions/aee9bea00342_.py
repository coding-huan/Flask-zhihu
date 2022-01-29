"""empty message

Revision ID: aee9bea00342
Revises: f5cbc7da37e5
Create Date: 2022-01-28 16:13:00.369559

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aee9bea00342'
down_revision = 'f5cbc7da37e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('answer',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('answer')
    # ### end Alembic commands ###
