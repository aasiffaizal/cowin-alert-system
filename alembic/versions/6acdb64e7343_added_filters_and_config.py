"""Added Filters and config

Revision ID: 6acdb64e7343
Revises: 147710f54a5b
Create Date: 2021-05-20 21:52:18.161648

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6acdb64e7343'
down_revision = '147710f54a5b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('alert_config',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('district_id', sa.Integer(), nullable=True),
    sa.Column('chat_id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['district_id'], ['district.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_alert_config_chat_id'), 'alert_config', ['chat_id'], unique=False)
    op.create_index(op.f('ix_alert_config_id'), 'alert_config', ['id'], unique=False)
    op.create_table('configured_filter',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('alert_config_id', sa.Integer(), nullable=True),
    sa.Column('filter', sa.Enum('Vaccine', 'Age', 'Dose', name='filters'), nullable=False),
    sa.Column('evaluator', sa.Enum('Equals', 'GreaterThan', 'LessThan', 'In', name='evaluators'), nullable=False),
    sa.Column('value', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['alert_config_id'], ['alert_config.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_configured_filter_id'), 'configured_filter', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_configured_filter_id'), table_name='configured_filter')
    op.drop_table('configured_filter')
    op.drop_index(op.f('ix_alert_config_id'), table_name='alert_config')
    op.drop_index(op.f('ix_alert_config_chat_id'), table_name='alert_config')
    op.drop_table('alert_config')
    # ### end Alembic commands ###
