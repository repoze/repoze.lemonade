from zope.component import getGlobalSiteManager
from zope.component import getAdapter
from zope.interface import directlyProvides

from repoze.lemonade.interfaces import IContentFactory

class dummy:
    def __init__(self, iface):
        directlyProvides(self, iface)

def create_content(iface, *arg, **kw):
    """ Create an instance of the content type related to ``iface``,
    by calling its factory, passing ``*arg`` and ``**kw`` to the factory.
    Raise a ComponentLookupError  if there is no content type related to 
    ``iface`` """
    factory = getAdapter(dummy(iface), IContentFactory)
    return factory(*arg, **kw)

def get_content_types():
    """ Return a sequence of interface objects that have been
    registered as content types. """
    types = []
    gsm = getGlobalSiteManager()
    for reg in gsm.registeredAdapters():
        if reg.provided is IContentFactory:
            types.append(reg.required[0])
    return types
        
