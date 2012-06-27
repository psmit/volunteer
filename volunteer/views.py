from pyramid.view import view_config


from .models import (
    DBSession,
    Team,
    User,
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