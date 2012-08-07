"""Add notified field

Revision ID: 260ed01cee8d
Revises: 5a28e8a113b3
Create Date: 2012-07-29 17:32:18.623062

"""

# revision identifiers, used by Alembic.
from alembic.ddl.base import ColumnDefault

revision = '260ed01cee8d'
down_revision = '5a28e8a113b3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('slotuser', sa.Column('notified', sa.Boolean(), nullable=False, server_default="0"))



def downgrade():
    op.drop_column('slotuser', 'notified')
