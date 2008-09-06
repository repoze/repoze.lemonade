from zope.interface import Interface

class IObjectEvent(Interface):
    """ An event involving a persistent object """
    
class IObjectModifiedEvent(IObjectEvent):
    """ An event type sent when an object is modified """
    
class IObjectAddedEvent(IObjectEvent):
    """ An event type sent when an object is added """

class IObjectRemovedEvent(IObjectEvent):
    """ An event type sent when an object is removed """
    
class IFolder(Interface):
    """ Folder """

