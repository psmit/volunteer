# coding=utf-8
import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import (
    DBSession,
    SmsDelivery,
    SmsMessagePart,
    Base,
    )

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        for sms_delivery in DBSession.query(SmsDelivery).all():
            message_part = DBSession.query(SmsMessagePart).filter(SmsMessagePart.message_id == sms_delivery.message_id).first()
            if message_part is not None:
                sms_delivery.sms_message_part = message_part