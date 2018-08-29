from rq import Queue

from webapp import services, worker
from webapp.statements import Actor, Verb, Object, Statement, Context, Result

xapi_url = 'https://alumnica.org/'
q = Queue(connection=worker.conn)


def login_statement(request, user, timestamp):
    """
    Xapi login statement constructor
    :param user: Current AuthUser
    :param timestamp: login timestamp
    """
    user_complete_name = user.first_name + ' ' + user.last_name
    actor = Actor(name=user_complete_name, email=user.email)
    verb = Verb(action='logged-in')
    object_id = xapi_url + 'login'
    object = Object(id=object_id, name='Alumnica')

    statement = Statement(timestamp=timestamp, actor=actor, verb=verb, object=object)
    q.enqueue(services.send, statement, timeout=200)


def register_statement(request, user, timestamp):
    """
    Xapi account register statement constructor
    :param user: Current AuthUser
    :param timestamp: register timestamp
    """
    user_complete_name = user.first_name + ' ' + user.last_name
    actor = Actor(name=user_complete_name, email=user.email)
    verb = Verb(action='registered')
    object_id = xapi_url + 'register'
    object = Object(id=object_id, name='Alumnica')

    statement = Statement(timestamp=timestamp, actor=actor, verb=verb, object=object)
    q.enqueue(services.send, statement, timeout=200)


def edited_profile(user, timestamp):
    """
    Xapi edit profile statement constructor
    :param user: Current AuthUser
    :param timestamp: activity timestamp
    """
    user_complete_name = user.first_name + ' ' + user.last_name
    actor = Actor(name=user_complete_name, email=user.email)
    verb = Verb(action='edited')
    object_id = xapi_url + 'edit_profile'
    object = Object(id=object_id, name='user_profile')

    statement = Statement(timestamp=timestamp, actor=actor, verb=verb, object=object)
    q.enqueue(services.send, statement, timeout=200)


def avatar_statement(user, avatar, timestamp):
    """
    Xapi change avatar statement constructor
    :param user: Current AuthUser
    :param avatar: Avatar image selected
    :param timestamp: activity timestamp
    :return:
    """
    user_complete_name = user.first_name + ' ' + user.last_name
    actor = Actor(name=user_complete_name, email=user.email)
    verb = Verb(action='selected')
    object_id = xapi_url + 'avatar/' + avatar
    object = Object(id=object_id, name='avatar_'+avatar)

    statement = Statement(timestamp=timestamp, actor=actor, verb=verb, object=object)
    q.enqueue(services.send, statement, timeout=200)


def logout_statement(request, user, timestamp):
    """
    Xapi logout statement constructor
    :param user: Current AuthUser
    :param timestamp: Logout timestamp
    """
    user_complete_name = user.first_name + ' ' + user.last_name
    actor = Actor(name=user_complete_name, email=user.email)
    verb = Verb(action='logged-out')
    object_id = xapi_url + 'logout'
    object = Object(id=object_id, name='Alumnica')

    statement = Statement(timestamp=timestamp, actor=actor, verb=verb, object=object)
    q.enqueue(services.send, statement, timeout=200)


def search_statement(user, string_searched, timestamp):
    """
    Xapi search statement constructor
    :param user: Current AuthUser
    :param string_searched: string
    :param timestamp: activity timestamp
    """
    user_complete_name = user.first_name + ' ' + user.last_name
    actor = Actor(name=user_complete_name, email=user.email)
    verb = Verb(action='searched')
    object_id = xapi_url + 'search'
    object = Object(id=object_id, name='Alumnica')
    result = Result(response=string_searched)

    statement = Statement(timestamp=timestamp, actor=actor, verb=verb, object=object, result=result)
    q.enqueue(services.send, statement, timeout=200)


def access_statement(request, object_name, timestamp):
    """
    Xapi page access statement constructor
    :param request: Containing current AuthUser
    :param object_name: Object type
    :param timestamp: activity timestamp
    """
    user_complete_name = request.user.first_name + ' ' + request.user.last_name
    actor = Actor(name=user_complete_name, email=request.user.email)
    verb = Verb(action='accessed')
    object_id = xapi_url + object_name
    object = Object(id=object_id, name=object_name)

    statement = Statement(timestamp=timestamp, actor=actor, verb=verb, object=object)
    q.enqueue(services.send, statement, timeout=200)


def access_statement_with_parent(request, object_type, object_name, parent_type, parent_name, tags_array, timestamp):
    """
    Xapi access to page with parent object
    :param request: Containing current AuthUser
    :param object_type: object type
    :param object_name: object name
    :param parent_type: parent object type
    :param parent_name: parent object name
    :param tags_array: object tags
    :param timestamp: activity timestamp
    """
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
    q.enqueue(services.send, statement, timeout=200)


def task_completed(user, object_type, object_name, parent_type, parent_name, tags_array, timestamp, score=None, max_score=None,
                   duration=None, completion=False):
    """
    Xapi completed task statement constructor
    :param user: Current AuthUser
    :param object_type: object type
    :param object_name: object name
    :param parent_type: parent object type
    :param parent_name: parent object name
    :param tags_array: object tags
    :param timestamp: activity timpestamp
    :param score: score obtained
    :param duration: duration
    """
    user_complete_name = user.first_name + ' ' + user.last_name
    actor = Actor(name=user_complete_name, email=user.email)
    verb = Verb(action='completed')
    object_id = '{}{}/{}'.format(xapi_url, object_type, object_name)
    object_type_url = '{}{}'.format(xapi_url, object_type)
    object = Object(id=object_id, name=object_name, type=object_type_url)
    parent_id = '{}{}/{}'.format(xapi_url, parent_type, parent_name)

    tags = []
    for tag in tags_array:
        tags.append('{}tag/{}'.format(xapi_url, tag))

    context = Context([parent_id], tags)
    if score is None:
        result = Result(response='{} completed'.format(object_type), completion=completion, duration=duration)
    else:
        result = Result(response='{} completed'.format(object_type), completion=completion, success=score >= 7,
                        raw_score=score, max_score=max_score, duration=duration)

    statement = Statement(timestamp=timestamp, actor=actor, verb=verb, object=object, context=context, result=result)
    q.enqueue(services.send, statement, timeout=200)


def h5p_task_completed(user, object_type, object_name, parent_type, parent_name, tags_array, timestamp, score=None, max_score=None,
                   duration=None):
    """
    Xapi completed task statement constructor
    :param user: Current AuthUser
    :param object_type: object type
    :param object_name: object name
    :param parent_type: parent object type
    :param parent_name: parent object name
    :param tags_array: object tags
    :param timestamp: activity timpestamp
    :param score: score obtained
    :param duration: duration
    """
    user_complete_name = user.first_name + ' ' + user.last_name
    actor = Actor(name=user_complete_name, email=user.email)
    verb = Verb(action='completed')
    object_id = '{}{}/{}'.format(xapi_url, object_type, object_name)
    object_type_url = '{}{}'.format(xapi_url, object_type)
    object = Object(id=object_id, name=object_name, type=object_type_url)
    parent_id = '{}{}/{}'.format(xapi_url, parent_type, parent_name)

    tags = []
    for tag in tags_array:
        tags.append('{}tag/{}'.format(xapi_url, tag))

    context = Context([parent_id], tags)
    if score is None:
        result = Result(response='{} completed'.format(object_type), completion=True, duration=duration)
    else:
        result = Result(response='{} completed'.format(object_type), completion=True, success=score == max_score,
                        raw_score=score, max_score=max_score, duration=duration)

    statement = Statement(timestamp=timestamp, actor=actor, verb=verb, object=object, context=context, result=result)
    q.enqueue(services.send, statement, timeout=200)


def answered_question_statement(user, question_instance, tags_array, timestamp, success):
    """
    Xapi answered question statement constructor
    :param user: Current AuthUser
    :param question_instance: question object
    :param tags_array: ODA tags
    :param timestamp: Evaluation submitted timestamp
    :param success: answer status
    """
    user_complete_name = user.first_name + ' ' + user.last_name
    actor = Actor(name=user_complete_name, email=user.email)
    verb = Verb(action='answered')
    object_id = '{}{}/{}'.format(xapi_url, 'question_answer', question_instance.type)
    object = Object(id=object_id, name=question_instance.type)
    parent_id = '{}{}/{}'.format(xapi_url, 'evaluation', question_instance.evaluation.name)
    tags = []
    for tag in tags_array:
        tags.append('{}tag/{}'.format(xapi_url, tag))

    context = Context([parent_id], tags)
    result = Result(response='Question: {}'.format(question_instance.sentence), success=success)
    statement = Statement(timestamp=timestamp, actor=actor, verb=verb, object=object, context=context, result=result)
    q.enqueue(services.send, statement, timeout=200)


def learning_experience_received(user, object_type, object_name, timestamp, gained_xp):
    """
    Xapi experience received for learning quiz statement constructor
    :param user: Current AuthUser
    :param object_type: object type
    :param object_name: object name
    :param timestamp: activity timestamp
    :param gained_xp: experience gained points
    """
    user_complete_name = user.first_name + ' ' + user.last_name
    actor = Actor(name=user_complete_name, email=user.email)
    verb = Verb(action='earned')
    object_id = '{}{}/{}'.format(xapi_url, object_type, object_name)
    object = Object(id=object_id, name=object_name)
    # result = Result(response='{} completed'.format(object_type), completion=True, success=True, raw_score=gained_xp)
    statement = Statement(timestamp=timestamp, actor=actor, verb=verb, object=object)
    q.enqueue(services.send, statement, timeout=200)


def task_experience_received(user, object_type, object_name, parent_type, parent_name, tags_array, timestamp,
                             gained_xp):
    """
    Xapi task experience received statement constructor
    :param user: Current AuthUser
    :param object_type: object type
    :param object_name: object name
    :param parent_type: parent object type
    :param parent_name: parent  object name
    :param tags_array: object tags array
    :param timestamp: activity timestamp
    :param gained_xp: gained experience points
    """
    user_complete_name = user.first_name + ' ' + user.last_name
    actor = Actor(name=user_complete_name, email=user.email)
    verb = Verb(action='earned')
    object_id = '{}{}/{}'.format(xapi_url, object_type, object_name)
    object = Object(id=object_id, name=object_name)
    parent_id = '{}{}/{}'.format(xapi_url, parent_type, parent_name)

    tags = []
    for tag in tags_array:
        tags.append('{}tag/{}'.format(xapi_url, tag))

    context = Context([parent_id], tags)

    # result = Result(response='{} completed'.format(object_type), completion=True, success=True, raw_score=gained_xp)

    statement = Statement(timestamp=timestamp, actor=actor, verb=verb, object=object, context=context)
    q.enqueue(services.send, statement, timeout=200)
