from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from deform import Form, ValidationFailure

from .libs import send_sms

from .models import (
    DBSession,
    Team,
    User,
    Sms,
    Event,
)
from .schemas import (
    SmsSchema,
    UserForm,
    UserTeamForm,
    EventForm,
)
from sqlalchemy.exc import IntegrityError

def add_underscore_versions_of_keys(d):
    for key in d.keys():
        if '-' in key:
            d[key.replace('-','_')] = d[key]

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

    events = DBSession.query(Event).all()
    return {'form_title': message,
            'events':events,
            'form': form}




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

@view_config(route_name='get_possible_users_team',renderer='json')
@view_config(route_name='get_possible_users', renderer='json')
def get_possible_users(request):
    query = DBSession.query(User)
    try:
        query = query.filter(~User.memberteams.any(Team.id == int(request.matchdict['team'])))
    except (ValueError,KeyError):
        pass

    return [(user.id,user.name) for user in query.all()]

def record_to_appstruct(self):
    return dict([(k, self.__dict__[k]) for k in sorted(self.__dict__) if '_sa_' != k[:4]])

@view_config(route_name='incoming_sms',renderer='sms.mako')
def incoming_sms(request):
    schema = SmsSchema()
    form = Form(schema, buttons=('submit',), method="GET")
    if 'messageId' in request.GET:
        try:
            add_underscore_versions_of_keys(request.GET)
            appstruct = form.validate(request.GET.items())
        except ValidationFailure, e:
            return {'project':'my project',
                    'form':e.render(),
                    'extra':'boo',
                    }

        sms = Sms()
        for key,value in appstruct.items():
            setattr(sms, key, value)
        DBSession.add(sms)

        if sms.text.strip().lower().startswith("test"):
            send_sms(sms.msisdn,'This SMS should be send from "UCC". Let Peter know if it\'s not',request.registry.settings,from_name="UCC")
            send_sms(sms.msisdn,'This SMS should be send from "+3584573950790". Let Peter know if it\'s not',request.registry.settings,from_name="3584573950790")
        else:
            send_sms(sms.msisdn,'This number is only used for sending messages, therefore your message could not be delivered.',request.registry.settings)

        return {'project':'my project',
                'form':'succes',
                'extra':'boo',
                }

    return {'project':'my project',
            'form':form.render(),
            'extra':request.registry.settings['sms.key'],
            }
#    return {'project':'my project'}
