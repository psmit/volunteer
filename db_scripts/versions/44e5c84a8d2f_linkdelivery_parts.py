"""empty message

Revision ID: 44e5c84a8d2f
Revises: 5eae5c591d4
Create Date: 2012-08-15 16:37:14.210644

"""

# revision identifiers, used by Alembic.
revision = '44e5c84a8d2f'
down_revision = '5eae5c591d4'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('smsdelivery', sa.Column('sms_message_part_id', sa.Integer(), sa.ForeignKey('smsmessagepart.id'), nullable=True))
    ### end Alembic commands ###



#    from volunteer.models import DBSession, SmsDelivery, SmsMessagePart
#
#    for sms_delivery in DBSession.query(SmsDelivery).all():
#        message_part = DBSession.query(SmsMessagePart).filter(SmsMessagePart.message_id == sms_delivery.message_id).first()
#        if message_part is not None:
#            sms_delivery.sms_message_part = message_part


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('smsdelivery', 'sms_message_part_id')
    ### end Alembic commands ###
