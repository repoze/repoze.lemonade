from zope.interface import Interface

from zope.component.interface import provideInterface

from zope.configuration.fields import GlobalObject
from zope.configuration.fields import GlobalInterface
from zope.component.zcml import handler

from repoze.lemonade.interfaces import IContentType
from repoze.lemonade.interfaces import IContentFactory

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
    _context.action(
        discriminator = ('content', type, IContentType),
        callable = provideInterface,
        args = ('', type, IContentType)
        )

    hammer = HammerFactoryFactory(factory)

    _context.action(
        discriminator = ('content', factory, type, IContentFactory),
        callable = handler,
        args = ('registerAdapter',
                hammer, (type,), IContentFactory, '', _context.info),
        )
