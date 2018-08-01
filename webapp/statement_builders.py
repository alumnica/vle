from django.urls import reverse_lazy

from webapp import services
from webapp.statements import Actor, Verb, Object, Statement


def login_statement(request, user, timestamp):
    user_complete_name = user.first_name + ' ' + user.last_name
    actor = Actor(name=user_complete_name, email=user.email)
    verb = Verb(action='logged-in')
    object_id = '{}://{}{}'.format(
        request.scheme,
        request.get_host(),
        reverse_lazy('login_view'))
    object = Object(id=object_id, name='Alumnica')

    statement = Statement(timestamp=timestamp, actor=actor, verb=verb, object=object)
    response = services.send(statement)


def register_statement(request, user, timestamp):
    user_complete_name = user.first_name + ' ' + user.last_name
    actor = Actor(name=user_complete_name, email=user.email)
    verb = Verb(action='registered')
    object_id = '{}://{}{}'.format(
        request.scheme,
        request.get_host(),
        reverse_lazy('signup_view'))
    object = Object(id=object_id, name='Alumnica')

    statement = Statement(timestamp=timestamp, actor=actor, verb=verb, object=object)
    response = services.send(statement)


def logout_statement(request, user, timestamp):
    user_complete_name = user.first_name + ' ' + user.last_name
    actor = Actor(name=user_complete_name, email=user.email)
    verb = Verb(action='logged-out')
    object_id = '{}://{}{}'.format(
        request.scheme,
        request.get_host(),
        reverse_lazy('logout_view'))
    object = Object(id=object_id, name='Alumnica')

    statement = Statement(timestamp=timestamp, actor=actor, verb=verb, object=object)
    response = services.send(statement)