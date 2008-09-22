from zope.interface import implements

from repoze.lemonade.interfaces import IObjectAddedEvent
from repoze.lemonade.interfaces import IObjectWillBeAddedEvent
from repoze.lemonade.interfaces import IObjectRemovedEvent
from repoze.lemonade.interfaces import IObjectWillBeRemovedEvent
from repoze.lemonade.interfaces import IObjectModifiedEvent

class ObjectAddedEvent(object):
    implements(IObjectAddedEvent)
    def __init__(self, object, parent, name):
        self.object = object
        self.parent = parent
        self.name = name

class ObjectWillBeAddedEvent(object):
    implements(IObjectWillBeAddedEvent)
    def __init__(self, object, parent, name):
        self.object = object
        self.parent = parent
        self.name = name

class ObjectRemovedEvent(object):
    implements(IObjectRemovedEvent)
    def __init__(self, object, parent, name):
        self.object = object
        self.parent = parent
        self.name = name

class ObjectWillBeRemovedEvent(object):
    implements(IObjectWillBeRemovedEvent)
    def __init__(self, object, parent, name):
        self.object = object
        self.parent = parent
        self.name = name
    
class ObjectModifiedEvent(object):
    implements(IObjectModifiedEvent)
    def __init__(self, object):
        self.object = object
