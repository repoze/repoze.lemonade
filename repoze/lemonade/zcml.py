from zope.interface import Interface
from zope.interface.interfaces import IInterface
from zope.interface import providedBy

from zope.component import getSiteManager

from zope.configuration.exceptions import ConfigurationError
from zope.configuration.fields import GlobalObject
from zope.configuration.fields import GlobalInterface

from zope.schema import TextLine

from repoze.lemonade.interfaces import IContentFactory
from repoze.lemonade.interfaces import IContent

def handler(methodName, *args, **kwargs):
    method = getattr(getSiteManager(), methodName)
    method(*args, **kwargs)


def addbase(iface1, iface2):
    if not iface2 in iface1.__iro__:
        iface1.__bases__ += (iface2,)
        return True
    return False

class HammerFactoryFactory(object):
    def __init__(self, factory):
        self.factory = factory

    def __call__(self, other):
        return self.factory

class IContentDirective(Interface):
    factory = GlobalObject(
        title=u"The factory that will create the content.",
        required=True
        )

    type = GlobalInterface(
        title=u"The type (an interface) that will be created by the factory",
        required=True)

def content(_context, factory, type):

    if not IInterface.providedBy(type):
        raise ConfigurationError(
            'The provided "type" argument (%r) is not an '
            'interface object (it does not inherit from '
            'zope.interface.Interface' % type)

    _context.action(
        discriminator = ('content', type, IContent),
        callable = addbase,
        args = (type, IContent),
        )

    hammer = HammerFactoryFactory(factory)

    _context.action(
        discriminator = ('content', factory, type, IContentFactory),
        callable = handler,
        args = ('registerAdapter',
                hammer, (type,), IContentFactory, '', _context.info),
        )

class IListItemDirective(Interface):
    provides = GlobalInterface(
        title=u"Provided interface",
        description=u"Interface provided by the utility.",
        required=True,
        )

    component = GlobalObject(
        title=u"Component to use",
        description=(u"Python name of the implementation object.  This"
                      " must identify an object in a module using the"
                      " full dotted name.  If specified, the"
                      " ``factory`` field must be left blank."),
        required=False,
        )

    factory = GlobalObject(
        title=u"Factory",
        description=(u"Python name of a factory which can create the"
                      " implementation object.  This must identify an"
                      " object in a module using the full dotted name."
                      " If specified, the ``component`` field must"
                      " be left blank."),
        required=False,
        )
    
    name = TextLine(
        title=u"Name",
        description=(u"Name of the registration.  This is used by"
                     " application code when locating a utility."),
        required=False,
        )

    title = TextLine(
        title=u"Title",
        description=u"Title for the registration.",
        required=False,
        )

    description = TextLine(
        title=u"Description",
        description=u"Description for the registration.",
        required=False,
        )

    sort_key = TextLine(
        title=u"Description",
        description=u"Description for the registration.",
        required=False,
        )

def listitem(_context, provides=None, component=None, factory=None, name=None,
             title=None, description=None, sort_key=0):

    if factory:
        if component:
            raise TypeError("Can't specify factory and component.")
        component = factory()

    if name is None:
        raise TypeError('name must be specified')

    if provides is None:
        provides = list(providedBy(component))
        if len(provides) == 1:
            provides = provides[0]
        else:
            raise TypeError("Missing 'provides' attribute")

    try:
        sort_key = int(sort_key)
    except (TypeError, ValueError):
        pass

    info = {'title':title, 'description':description, 'sort_key':sort_key}

    _context.action(
        discriminator = ('utility', provides, name),
        callable = handler,
        args = ('registerUtility', component, provides, name, info),
        )

