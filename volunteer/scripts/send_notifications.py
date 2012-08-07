# coding=utf-8
from datetime import datetime, timedelta
import logging
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
    Event,
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

    logger = logging.getLogger(__name__)
    with transaction.manager:
        events = DBSession.query(Event).filter(datetime.now() < Event.date).filter(Event.date < datetime.now() + timedelta(hours=17)).all()

        for e in events:
            for slot in e.slots:
                for slotuser in slot.slotusers:
                    user = slotuser.user
                    if user.phone is not None and not slotuser.notified:
                        sms = send_sms(user.phone,"Hey %s, just a reminder that you are on the roster for Sound in UCC Leppavaara tomorrow 8.30!" % user.name.split()[0],settings, from_name="UCC Sound")
                        logger.info("Send sms to %s" % user.name)
                        print "Send sms to %s" % user.name
                        slotuser.notified = True
                        slotuser.notify_sms = sms
#                        DBSession.add(slotuser)

