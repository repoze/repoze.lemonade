from zope.interface import Interface
from zope.interface.interfaces import IInterface

class IObjectEvent(Interface):
    """ An event involving a persistent object """
    
class IObjectModifiedEvent(IObjectEvent):
    """ An event type sent when an object is modified """
    
class IObjectAddedEvent(IObjectEvent):
    """ An event type sent when an object is added """

class IObjectAboutToBeRemovedEvent(IObjectEvent):
    """ An event type sent before an object is removed """

class IObjectRemovedEvent(IObjectEvent):
    """ An event type sent when an object is removed """

class IContentFactory(Interface):
    """ Content factory """
    def __call__(*arg, **kw):
        """ Return a content instance  """
    
class IContentType(IInterface):
    """ Content """

class IFolder(Interface):
    """ Folder """

