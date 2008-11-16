from zope.component import getGlobalSiteManager
from zope.component import getAdapter
from zope.interface import directlyProvides

from repoze.lemonade.interfaces import IContentFactory

class provides:
    def __init__(self, iface):
        directlyProvides(self, iface)

_marker = ()

def create_content(iface, *arg, **kw):
    """ Create an instance of the content type related to ``iface``,
    by calling its factory, passing ``*arg`` and ``**kw`` to the factory.
    Raise a ComponentLookupError  if there is no content type related to 
    ``iface`` """
    factory = getAdapter(provides(iface), IContentFactory)
    return factory(*arg, **kw)

def get_content_types(context=_marker):
    """ Return a sequence of interface objects that have been
    registered as content types.  If ``context`` is used, return only
    the content_type interfaces which are provided by the context."""
    types = []
    gsm = getGlobalSiteManager()
    for reg in gsm.registeredAdapters():
        if reg.provided is IContentFactory:
            iface = reg.required[0]
            if context is _marker:
                types.append(iface)
            elif iface.providedBy(context):
                types.append(iface)
    return types
        
def get_content_type(context):
    types = get_content_types(context)
    if len(types) > 1:
        raise ValueError('%r has more than one content type (%s)' %
                         (context, types))
    if not types:
        raise ValueError('%s is not content' % context)
        
    return types[0]

def is_content(model):
    """ Return True if the model object provides any interface
    registered as a content type, False otherwise. """
    return bool(get_content_types(model))

