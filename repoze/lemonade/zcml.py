from zope.interface import Interface
from zope.interface.interfaces import IInterface

from zope.component.interface import provideInterface

from zope.configuration.exceptions import ConfigurationError
from zope.configuration.fields import GlobalObject
from zope.configuration.fields import GlobalInterface
from zope.component.zcml import handler

from repoze.lemonade.interfaces import IContentType
from repoze.lemonade.interfaces import IContentFactory
from repoze.lemonade.interfaces import IContent

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
        discriminator = ('content', type, IContentType),
        callable = provideInterface,
        args = ('', type, IContentType)
        )

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
