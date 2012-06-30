from pyramid.view import view_config
from deform import Form, ValidationFailure

from .models import (
    DBSession,
    Team,
    User,
    Sms,
)
from .schemas import (
    SmsSchema,
)

@view_config(route_name='view_teams', renderer='teams.mako')
def view_teams(request):
    teams = DBSession.query(Team).all()
    return {'project':'my project',
            'teams':teams}

@view_config(route_name='get_possible_users', renderer='json')
def get_possible_users(request):
    users = DBSession.query(User).all()
    users_json = []
    for u in users:
        users_json.append({
            'id': u.id,
            'name': u.name,
        })
    return users_json

def record_to_appstruct(self):
    return dict([(k, self.__dict__[k]) for k in sorted(self.__dict__) if '_sa_' != k[:4]])

@view_config(route_name='incoming_sms',renderer='sms.mako')
def incoming_sms(request):
    schema = SmsSchema()
    form = Form(schema, buttons=('submit',), method="GET")
    if 'messageId' in request.GET:
        try:
            appstruct = form.validate(request.GET.items())
        except ValidationFailure, e:
            return {'project':'my project',
                    'form':e.render()}

        sms = Sms()
        for key,value in appstruct.items():
            setattr(sms, key, value)
        DBSession.add(sms)

        return {'project':'my project',
                'form':'succes'}

    return {'project':'my project',
            'form':form.render()}
#    return {'project':'my project'}