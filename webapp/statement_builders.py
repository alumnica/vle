from django.urls import reverse_lazy

from webapp import services
from webapp.statements import Actor, Verb, Object, Statement, Context

xapi_url = 'http://alumnica.org/'


def login_statement(request, user, timestamp):
    user_complete_name = user.first_name + ' ' + user.last_name
    actor = Actor(name=user_complete_name, email=user.email)
    verb = Verb(action='logged-in')
    object_id = xapi_url + 'login'
    object = Object(id=object_id, name='Alumnica')

    statement = Statement(timestamp=timestamp, actor=actor, verb=verb, object=object)
    response = services.send(statement)


def register_statement(request, user, timestamp):
    user_complete_name = user.first_name + ' ' + user.last_name
    actor = Actor(name=user_complete_name, email=user.email)
    verb = Verb(action='registered')
    object_id = xapi_url + 'register'
    object = Object(id=object_id, name='Alumnica')

    statement = Statement(timestamp=timestamp, actor=actor, verb=verb, object=object)
    response = services.send(statement)


def logout_statement(request, user, timestamp):
    user_complete_name = user.first_name + ' ' + user.last_name
    actor = Actor(name=user_complete_name, email=user.email)
    verb = Verb(action='logged-out')
    object_id = xapi_url + 'logout'
    object = Object(id=object_id, name='Alumnica')

    statement = Statement(timestamp=timestamp, actor=actor, verb=verb, object=object)
    response = services.send(statement)


def access_statement(request, object_name, timestamp):
    user_complete_name = request.user.first_name + ' ' + request.user.last_name
    actor = Actor(name=user_complete_name, email=request.user.email)
    verb = Verb(action='accessed')
    object_id = xapi_url + object_name
    object = Object(id=object_id, name=object_name)

    statement = Statement(timestamp=timestamp, actor=actor, verb=verb, object=object)
    response = services.send(statement)


def access_statement_with_parent(request, object_type, object_name, parent_type, parent_name, timestamp):
    user_complete_name = request.user.first_name + ' ' + request.user.last_name
    actor = Actor(name=user_complete_name, email=request.user.email)
    verb = Verb(action='accessed')
    object_id = '{}{}/{}'.format(xapi_url, object_type, object_name)
    object = Object(id=object_id, name=object_name)
    parent_id = '{}{}/{}'.format(xapi_url, parent_type, parent_name)
    context = Context([parent_id])

    statement = Statement(timestamp=timestamp, actor=actor, verb=verb, object=object, context=context)
    response = services.send(statement)