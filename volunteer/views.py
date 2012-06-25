from pyramid.view import view_config


from .models import (
    DBSession,
    Team,
)

@view_config(route_name='view_teams', renderer='teams.mako')
def view_teams(request):
    teams = DBSession.query(Team).all()
    return {'project':'my project',
            'teams':teams}