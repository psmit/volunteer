from pyramid.config import Configurator

from sqlalchemy import engine_from_config

from .models import DBSession

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    config = Configurator(settings=settings)

    config.add_static_view(name='static', path='../static', cache_max_age=3600)
    config.add_route('view_teams', '/teams')
    config.add_route('view_users', '/users')
    config.add_route('edit_users', '/users/{id}')
    config.add_route('add_team_member', '/teams/add_member',xhr=True)
    config.add_route('add_user', '/users/add', xhr=True)
    config.add_route('get_possible_users', '/json/users', xhr=True)
    config.add_route('get_possible_users_team','/json/users/team/{team}', xhr=True)
    config.add_route('incoming_sms', '/sms')
    config.scan()
    return config.make_wsgi_app()