from datetime import datetime
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
        u_peter = User("Peter Smit", "peter@smitmail.eu","0442182700")
        u_akin = User("Akin Savage")
        u_martin = User("Martin Kallenbach")
        u_aschelew = User("Aschelew")
        u_francis = User("Francis")
        u_lauri = User("Lauri Laukkanen")
        u_mark = User("Mark Laukkanen")

        DBSession.add(u_peter)
        DBSession.add(u_akin)
        DBSession.add(u_martin)
        DBSession.add(u_aschelew)
        DBSession.add(u_francis)

        DBSession.add(u_lauri)
        DBSession.add(u_mark)

        t_sound = Team("Sound")
        t_media = Team("Media")

        DBSession.add(t_sound)
        DBSession.add(t_media)

        t_sound.leader = u_peter
        t_media.leader = u_lauri

        t_sound.members = [u_peter,u_akin,u_martin,u_aschelew,u_francis]
        t_media.members = [u_lauri,u_mark]

        e_1 = Event("Sunday July 1st", datetime(2012,7,1,10))
        e_2 = Event("Sunday July 8th", datetime(2012,7,8,10))

        DBSession.add(e_1)
        DBSession.add(e_2)

        s_1_sound = Slot()
#        s_1_media = Slot(e_1,t_media)
#        s_2_sound = Slot(e_2,t_sound)
#        s_2_media = Slot(e_2,t_media)

        DBSession.add(s_1_sound)
#        DBSession.add(s_1_media)
#        DBSession.add(s_2_sound)
#        DBSession.add(s_2_media)
        s_1_sound.team = t_sound
        s_1_sound.event = e_1

        sl = SlotUser()

        sl.slot = s_1_sound
        sl.available = "Unknown"
        sl.selected = "NotSelected"

        u_peter.slots.append(sl)


#        DBSession.add(s_2_sound)
#        DBSession.add(s_2_media)
#    with transaction.manager:
#        model = Page('FrontPage', 'This is the front page')
#        DBSession.add(model)
