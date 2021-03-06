from calendar import monthrange
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.settings import aslist
from pyramid.view import view_config, view_defaults
from datetime import date, time, datetime, timedelta

from .libs import (
    send_sms,
    sms_saldo,
)

from .models import (
    DBSession,
    Team,
    User,
    SmsMessage,
    Sms,
    Event,
    Slot,
    SlotUser,
    SmsDelivery,
    SmsMessagePart,
)
from .forms import (
    SmsDeliveryForm,
    UserForm,
    UserTeamForm,
    EventForm,
    GenEventForm,
    SmsForm,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import and_

def add_underscore_versions_of_keys(d):
    for key in d.keys():
        if '-' in key:
            d[key.replace('-','_')] = d[key]


@view_config(route_name='index', renderer='index.mako')
def index(request):

    events = DBSession.query(Event).filter(
        and_(Event.date >= datetime.now())).order_by(Event.date).limit(4).all()

    smses = DBSession.query(SmsMessage).order_by(SmsMessage.id.desc()).limit(10).all()

    return {'events': events,
            'smses': smses,
            'saldo': sms_saldo(request.registry.settings),
            }


@view_config(route_name='view_teams', renderer='teams.mako')
def view_teams(request):
    teams = DBSession.query(Team).all()
    return {'teams':teams,
            'form':UserTeamForm()}

@view_config(route_name='edit_users', renderer='users.mako')
@view_config(route_name='view_users', renderer='users.mako')
def view_users(request):
    try:
        user = DBSession.query(User).get(int(request.matchdict['id']))
        message = "Edit details for %s" % user.name
    except (ValueError,KeyError,AttributeError):
        user = User()
        message = "Add new user"

    form = UserForm(request.POST,user)
    if request.method == 'POST' and form.validate():
        form.populate_obj(user)
        try:
            DBSession.add(user)
        except IntegrityError, e:

            pass
        #form = UserForm()
        return HTTPFound('/users')

    users = DBSession.query(User).all()
    return {'form_title': message,
            'users':users,
            'form': form}


@view_config(route_name='edit_events', renderer='events.mako')
@view_config(route_name='view_events', renderer='events.mako')
def view_events(request):
    try:
        event = DBSession.query(Event).get(int(request.matchdict['id']))
        message = "Edit details for %s" % event.title
    except (ValueError,KeyError,AttributeError):
        event = Event()
        message = "Add new event"

    form = EventForm(request.POST,event)
    if request.method == 'POST' and form.validate():
        form.populate_obj(event)
        try:
            DBSession.add(event)
        except IntegrityError, e:

            pass
            #form = UserForm()
        return HTTPFound('/events')

    gen_form = GenEventForm(request.POST)
    if request.method == 'POST' and gen_form.validate():
        test_date = gen_form.data['start_date']
        try:
            h,m = [int(a) for a in gen_form.data['gen_time'].split(':',1)]
        except ValueError:
            h,m = 10,0
        the_time = time(h,m)
        while test_date <= gen_form.data['end_date']:
            if test_date.isoweekday() == gen_form.data['gen_day']:
                event_date = datetime.combine(test_date,the_time)
                other_events = DBSession.query(Event).filter(Event.date == event_date).all()
                if len(other_events) == 0:

                    new_event = Event()
                    new_event.date = event_date
                    new_event.title = event_date.strftime(gen_form.data['gen_title'])
                    DBSession.add(new_event)

            test_date = test_date + timedelta(days=1)

        return HTTPFound('/events')

    events = DBSession.query(Event).all()
    return {'form_title': message,
            'events':events,
            'form': form,
            'gen_form': gen_form}

@view_config(route_name='view_event', renderer='viewevent.mako')
def view_event(request):
    try:
        event = DBSession.query(Event).get(int(request.matchdict['id']))
    except (ValueError,KeyError,AttributeError):
        return HTTPFound('/events')

    query = DBSession.query(Team)
    query = query.filter(~Team.slots.any(Slot.event_id == int(request.matchdict['id'])))

    teams = query.all()

    return {'event': event,
            'other_teams': teams,
            }

@view_config(route_name='overview_m',renderer='overview.mako')
@view_config(route_name='overview_y',renderer='overview.mako')
@view_config(route_name='overview', renderer='overview.mako')
def overview(request):
    year = month = None
    try:
        month = int(request.matchdict['month'])
        year = int(request.matchdict['year'])
    except (KeyError,ValueError):
        pass

    if month is None or not (1 <= month <= 12):
        month = date.today().month

    if year is None:
        year = date.today().year

    num_days = monthrange(year, month)[1]
    start_date = date(year, month, 1)
    end_date = date(year, month, num_days)

    events = DBSession.query(Event).filter(
        and_(Event.date >= start_date, Event.date <= end_date)).all()

    return {'events': events,
            'month': month,
            'year': year,
            }

@view_config(route_name='del_slot',renderer='json')
def del_slot(request):
    try:
        slot = DBSession.query(Slot).get(int(request.GET['slot']))
        for slotuser in slot.slotusers:
            DBSession.delete(slotuser)
        DBSession.delete(slot)

    except (ValueError,KeyError,AttributeError):
        return {'success': False}

@view_config(route_name='add_slot',renderer='json')
def add_slot(request):
    try:
        team = DBSession.query(Team).get(int(request.GET['team']))
        event = DBSession.query(Event).get(int(request.GET['event']))

        slot = Slot()
        slot.event = event
        slot.team = team
        DBSession.add(slot)

        return {'success': True,
                'team': team.name,
                'slot.id': slot.id,
                }

    except (ValueError,KeyError,AttributeError):
        return {'success': False,
                'error': 'Wrong arguments given'}

@view_config(route_name='add_slotuser',renderer='json')
def add_slotuser(request):
    try:
        slot = DBSession.query(Slot).get(int(request.GET['slot']))
        user = DBSession.query(User).get(int(request.GET['user']))

        slotuser = SlotUser()
        slotuser.slot=slot
        slotuser.user = user
        slotuser.available = "Unknown"
        slotuser.selected = "NotSelected"
        DBSession.add(slotuser)

        return {'success': True}

    except (ValueError,KeyError,AttributeError):
        return {'success': False}

@view_config(route_name='del_slotuser',renderer='json')
def del_slotuser(request):
    try:
        slotuser =  DBSession.query(SlotUser).get((int(request.GET['slot']),int(request.GET['user'])))
        DBSession.delete(slotuser)
        return {'success': True}

    except (ValueError,KeyError,AttributeError):
        return {'success': False}

@view_config(route_name='add_team_member',renderer='json')
def add_team_member(request):
    if 'team' in request.GET and 'user' in request.GET:
        try:
            team_id = int(request.GET['team'])
            user_id = int(request.GET['user'])

            team = DBSession.query(Team).get(team_id)
            user = DBSession.query(User).get(user_id)
            team.members.append(user)

            return {'success': True,
                    'user_name': user.name}

        except ValueError:
            return {'success': False,
                    'error': 'Wrong arguments given'}

    return {'success': False,
            'error': 'Too little arguments given'}

@view_defaults(route_name='get_possible_users', renderer='json')
class UserCandidateFinder(object):
    def __init__(self,request):
        self.request = request

    def _format(self,users):
        return [(user.id,user.name) for user in users]

    @view_config(match_param='selection=slotevent')
    def slotevent(self):
        query = DBSession.query(User)
        try:
            slot = DBSession.query(Slot).get(int(self.request.matchdict['id']))
            query = query.filter(User.memberteams.any(Team.id == slot.team_id))
        except (ValueError,KeyError):
            pass

        return self._format(query.all())

    @view_config(match_param='selection=team')
    def team(self):
        query = DBSession.query(User)
        try:
            query = query.filter(~User.memberteams.any(Team.id == int(self.request.matchdict['id'])))
        except (ValueError,KeyError):
            pass

        return self._format(query.all())


def record_to_appstruct(self):
    return dict([(k, self.__dict__[k]) for k in sorted(self.__dict__) if '_sa_' != k[:4]])

@view_config(route_name='incoming_delivery', renderer='json')
def incoming_delivery(request):
    if request.remote_addr not in aslist(request.registry.settings['sms.allowed_ips']):
        return HTTPNotFound()
    add_underscore_versions_of_keys(request.GET)
    request.GET['message_id'] = request.GET['messageId']
    form = SmsDeliveryForm(request.GET)

    if request.method == 'GET' and form.validate():
        sd = SmsDelivery()
        form.populate_obj(sd)
        DBSession.add(sd)

        message_part = DBSession.query(SmsMessagePart).filter(SmsMessagePart.message_id == sd.message_id).first()
        if message_part is not None:
            sd.sms_message_part = message_part
    return {}


@view_config(route_name='incoming_sms',renderer='json')
def incoming_sms(request):
    if request.remote_addr not in aslist(request.registry.settings['sms.allowed_ips']):
        return HTTPNotFound()
    add_underscore_versions_of_keys(request.GET)
    form = SmsForm(request.GET)

    if request.method == 'GET' and form.validate():
        sms = Sms()
        form.populate_obj(sms)
        DBSession.add(sms)

        if sms.text.strip().lower().startswith("test"):
            send_sms(sms.msisdn,'This SMS should be send from "UCC Sound". Let Peter know if it\'s not',request.registry.settings,from_name="UCC Sound")
            send_sms(sms.msisdn,'This SMS should be send from "+3584573950790". Let Peter know if it\'s not',request.registry.settings,from_name="3584573950790")
        else:
            send_sms(sms.msisdn,'This number is only used for sending messages, therefore your message could not be delivered.',request.registry.settings)

    return {}

