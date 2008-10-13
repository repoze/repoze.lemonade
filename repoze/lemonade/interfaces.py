from zope.interface import Interface
from zope.interface.interfaces import IInterface

class IContentType(IInterface):
    """ Interface type representing a content type """

class IContentFactory(Interface):
    """ Content factory """
    def __call__(*arg, **kw):
        """ Return a content instance  """
    
