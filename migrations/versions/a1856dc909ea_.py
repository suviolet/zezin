"""empty message

Revision ID: a1856dc909ea
Revises:
Create Date: 2020-03-02 12:36:29.629364

"""
import geoalchemy2
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'a1856dc909ea'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('partner',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('trading_name', sa.String(length=50), nullable=False),
    sa.Column('owner_name', sa.String(length=50), nullable=False),
    sa.Column('document', sa.String(length=50), nullable=False),
    sa.Column('coverage_area', geoalchemy2.types.Geometry(geometry_type='MULTIPOLYGON'), nullable=True),
    sa.Column('address', geoalchemy2.types.Geometry(geometry_type='POINT'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('document')
    )


def downgrade():
    op.drop_table('partner')
