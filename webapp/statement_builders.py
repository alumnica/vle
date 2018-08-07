
from webapp import services
from webapp.statements import Actor, Verb, Object, Statement, Context, Result

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


def edited_profile(user, timestamp):
    user_complete_name = user.first_name + ' ' + user.last_name
    actor = Actor(name=user_complete_name, email=user.email)
    verb = Verb(action='edited')
    object_id = xapi_url + 'edit_profile'
    object = Object(id=object_id, name='user_profile')

    statement = Statement(timestamp=timestamp, actor=actor, verb=verb, object=object)
    response = services.send(statement)


def avatar_statement(user, avatar, timestamp):
    user_complete_name = user.first_name + ' ' + user.last_name
    actor = Actor(name=user_complete_name, email=user.email)
    verb = Verb(action='modified')
    object_id = xapi_url + 'avatar/' + avatar
    object = Object(id=object_id, name='avatar')

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


def access_statement_with_parent(request, object_type, object_name, parent_type, parent_name, tags_array, timestamp):
    user_complete_name = request.user.first_name + ' ' + request.user.last_name
    actor = Actor(name=user_complete_name, email=request.user.email)
    verb = Verb(action='accessed')
    object_id = '{}{}/{}'.format(xapi_url, object_type, object_name)
    object = Object(id=object_id, name=object_name)
    parent_id = '{}{}/{}'.format(xapi_url, parent_type, parent_name)

    tags = []
    for tag in tags_array:
        tags.append('{}tag/{}'.format(xapi_url, tag))

    context = Context([parent_id], tags)

    statement = Statement(timestamp=timestamp, actor=actor, verb=verb, object=object, context=context)
    response = services.send(statement)


def task_completed(user, object_type, object_name, parent_type, parent_name, tags_array, timestamp, score=None):
    user_complete_name = user.first_name + ' ' + user.last_name
    actor = Actor(name=user_complete_name, email=user.email)
    verb = Verb(action='completed')
    object_id = '{}{}/{}'.format(xapi_url, object_type, object_name)
    object = Object(id=object_id, name=object_name)
    parent_id = '{}{}/{}'.format(xapi_url, parent_type, parent_name)

    tags = []
    for tag in tags_array:
        tags.append('{}/tag/{}'.format(xapi_url, tag))

    context = Context([parent_id], tags)
    if score is None:
        result = Result(response='{} completed'.format(object_type), completion=True)
    else:
        result = Result(response='{} completed'.format(object_type), completion=True, success=score >= 7, raw_score=score)
    statement = Statement(timestamp=timestamp, actor=actor, verb=verb, object=object, context=context, result=result)
    response = services.send(statement)


def learning_experience_received(user, object_type, object_name, timestamp, gained_xp):
    user_complete_name = user.first_name + ' ' + user.last_name
    actor = Actor(name=user_complete_name, email=user.email)
    verb = Verb(action='received')
    object_id = '{}{}/{}'.format(xapi_url, object_type, object_name)
    object = Object(id=object_id, name=object_name)
    result = Result(response='{} completed'.format(object_type), completion=True, success=True, raw_score=gained_xp)
    statement = Statement(timestamp=timestamp, actor=actor, verb=verb, object=object, result=result)
    response = services.send(statement)


def task_experience_received(user, object_type, object_name, parent_type, parent_name, tags_array, timestamp, gained_xp):
    user_complete_name = user.first_name + ' ' + user.last_name
    actor = Actor(name=user_complete_name, email=user.email)
    verb = Verb(action='received')
    object_id = '{}{}/{}'.format(xapi_url, object_type, object_name)
    object = Object(id=object_id, name=object_name)
    parent_id = '{}{}/{}'.format(xapi_url, parent_type, parent_name)

    tags = []
    for tag in tags_array:
        tags.append('{}/tag/{}'.format(xapi_url, tag))

    context = Context([parent_id], tags)
    result = Result(response='{} completed'.format(object_type), completion=True, success=True, raw_score=gained_xp)
    statement = Statement(timestamp=timestamp, actor=actor, verb=verb, object=object, context=context, result=result)
    response = services.send(statement)