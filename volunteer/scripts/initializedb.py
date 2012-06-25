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
    Slot,
    SlotUser,
    User,
    Base,
    Team,
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
        u = User()
        u.name = "Peter Smit"
        u.email = "peter@smitmail.eu"
        u.phone = "0442182700"
        DBSession.add(u)

        u = User()
        u.name = "Lauri Laukkanen"
        DBSession.add(u)

        u = User()
        u.name = "Akin Savage"
        DBSession.add(u)

        u = User()
        u.name = "Mark Laukkanen"
        DBSession.add(u)

        t = Team()
        t.name = "Sound"
        DBSession.add(t)

        t = Team()
        t.name = "Media"
        DBSession.add(t)



#    with transaction.manager:
#        model = Page('FrontPage', 'This is the front page')
#        DBSession.add(model)
