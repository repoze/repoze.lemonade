from zope.interface import Interface
from zope.interface.interfaces import IInterface

class IContentType(IInterface):
    """ Interface meta-type representing a content type """

class IContentFactory(Interface):
    """ Content factory """
    def __call__(*arg, **kw):
        """ Return a content instance  """
    
class IContent(Interface):
    """ Marker interface appended to the ``__bases__`` of another
    interface when it is declared to be content via the ZCML
    ``lemonade:content`` directive"""

class IContentTypeCache(Interface):
    """ Marker interface used internally by get_content_types as the
    type used for a utility registration that acts as a content type
    cache """
    
