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
    Base,
    )
from ..libs import send_sms

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
#        events = DBSession.query(Event).filter(datetime.now() < Event.date).filter(Event.date < datetime.now() + timedelta(hours=17)).all()

        send_sms("358442182700","Hello from meHello from meHello from meHello from meHello from meHello from meHello from meHello from meHello from meHello from meHello from meHello from meHello from meHello from meHello from me",settings,from_name="UCC Sound")

