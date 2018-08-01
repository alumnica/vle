import json

theVerbs = {
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
}


def ComplexHandler(Obj):
    if hasattr(Obj, 'toJSON'):
        return Obj.toJSON()
    else:
        raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(Obj), repr(Obj)))


class Actor:
    def __init__(self, name, email):
        self.name = name
        self.mbox = 'mailto:'+email

    def toJSON(self):
        return self.__dict__


class Display:
    def __init__(self, action):
        self.en = action

    def toJSON(self):
        return self.__dict__


class Verb:
    def __init__(self, action):
        self.id = theVerbs[action]
        self.display = Display(action=action)

    def toJSON(self):
        return self.__dict__


class Definition:
    def __init__(self, name):
        self.name = Display(name)

    def toJSON(self):
        return self.__dict__


class Object:
    def __init__(self, id, name):
        self.id = id
        self.definition = Definition(name=name)

    def toJSON(self):
        return self.__dict__


class Parent:
    def __init__(self, id):
        self.id = id

    def toJSON(self):
        return self.__dict__


class ContextActivities:
    parent = []

    def __init__(self, parents):
        for id in parents:
            self.parent.append(Parent(id))

    def toJSON(self):
        parent = json.loads(json.dumps(self.parent, default=ComplexHandler))
        return {'parent': parent}


class Context:
    def __init__(self, parents):
        self.contextActivities = ContextActivities(parents=parents)

    def toJSON(self):
        return self.__dict__


class Score:
    def __init__(self, raw_score):
        self.raw = raw_score

    def toJSON(self):
        return self.__dict__


class Result:
    def __init__(self, response, completion=None, success=None, raw_score=None):
        self.response = response
        if completion is not None:
            self.completion = completion
        if success is not None:
            self.success = success
        if raw_score is not None:
            self.score = Score(raw_score=raw_score)

    def toJSON(self):
        return self.__dict__



class Statement:
    def __init__(self, timestamp, actor, verb, object, context=None, result=None):
        self.timestamp = timestamp
        self.actor = actor
        self.verb = verb
        self.object = object
        if context is not None:
            self.context = context
        if result is not None:
            self.result = result

    def toJSON(self):
        return self.__dict__
