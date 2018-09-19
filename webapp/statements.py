import json

xapi_verbs = {
    "registered": "http://adlnet.gov/expapi/verbs/registered",
    "accessed": "https://w3id.org/xapi/dod-isd/verbs/accessed",
    "selected": "https://w3id.org/xapi/dod-isd/verbs/selected",
    "highlighted": "https://w3id.org/xapi/adb/verbs/highlighted",
    "launched": "https://w3id.org/xapi/dod-isd/verbs/launched",
    "previewed": "http://id.tincanapi.com/verb/previewed",
    "initialized": "http://adlnet.gov/expapi/verbs/initialized",
    "completed": "http://adlnet.gov/expapi/verbs/completed",
    "received": "https://w3id.org/xapi/dod-isd/verbs/received",
    "edited": "https://w3id.org/xapi/dod-isd/verbs/edited",
    "modified": "https://w3id.org/xapi/dod-isd/verbs/modified",
    "searched": "https://w3id.org/xapi/dod-isd/verbs/searched",
    "logged-in": "https://w3id.org/xapi/adl/verbs/logged-in",
    "logged-out": "https://w3id.org/xapi/adl/verbs/logged-out",
    "answered": "http://adlnet.gov/expapi/verbs/answered",
    "earned": "https://registry.tincanapi.com/#uri/verb/441",
}


def ComplexHandler(obj):
    """
    Object to_json method caller
    """
    if hasattr(obj, 'to_json'):
        return obj.to_json()
    else:
        raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj)))


class Actor:
    """
    Actor object
    """
    def __init__(self, name, email):
        self.name = name
        self.mbox = 'mailto:' + email

    def to_json(self):
        return self.__dict__


class Display:
    """
    Display object containing language
    """
    def __init__(self, action):
        self.en = action

    def to_json(self):
        return self.__dict__


class Verb:
    """
    Verb object
    """
    def __init__(self, action):
        self.id = xapi_verbs[action]
        self.display = Display(action=action)

    def to_json(self):
        return self.__dict__


class Definition:
    """
    Definition object
    """
    def __init__(self, name, type):
        self.name = Display(name)
        if type is not None:
            self.type = type

    def to_json(self):
        return self.__dict__


class Object:
    """
    Xapi object
    """
    def __init__(self, id, name, type=None):
        self.id = id
        self.definition = Definition(name=name, type=type)

    def to_json(self):
        return self.__dict__


class ContextID:
    """
    Context url id object
    """
    def __init__(self, id):
        self.id = id

    def to_json(self):
        return self.__dict__


class ContextActivities:
    """
    Context activities array object
    """
    parent = []
    other = []

    def __init__(self, parents, tags):
        self.parent = []
        self.other = []
        for id in parents:
            self.parent.append(ContextID(id))
        for id in tags:
            self.other.append((ContextID(id)))

    def to_json(self):
        other = json.loads(json.dumps(self.other, default=ComplexHandler))
        parent = json.loads(json.dumps(self.parent, default=ComplexHandler))
        return {'parent': parent, 'other': other}


class Context:
    """
    Context object
    """
    def __init__(self, parents, tags):
        self.contextActivities = ContextActivities(parents=parents, tags=tags)

    def to_json(self):
        return self.__dict__


class Score:
    """
    Score object containing raw score
    """
    def __init__(self, raw_score, max_score=None):
        self.raw = raw_score
        if max_score is not None:
            self.max = max_score

    def to_json(self):
        return self.__dict__


class Result:
    """
    Result object
    """
    def __init__(self, response, completion=None, success=None, raw_score=None, max_score=None, duration=None):
        self.response = response
        if completion is not None:
            self.completion = completion
        if success is not None:
            self.success = success
        if raw_score is not None:
            if max_score is not None:
                self.score = Score(raw_score=raw_score, max_score=max_score)
            else:
                self.score = Score(raw_score=raw_score)
        if duration is not None:
            self.duration = duration

    def to_json(self):
        return self.__dict__


class Statement:
    """
    Statement object
    """
    def __init__(self, timestamp, actor, verb, object, context=None, result=None):
        self.timestamp = timestamp
        self.actor = actor
        self.verb = verb
        self.object = object
        if context is not None:
            self.context = context
        if result is not None:
            self.result = result

    def to_json(self):
        return self.__dict__
