from zope.component import getSiteManager

from repoze.lemonade.interfaces import IContentFactory

def registerContentFactory(factory, iface):
    """ Registers a lemonade ``IContentFactory`` (so it can be later
    looked up by ``create_content`` or ``get_content_types``).  The
    first argument, ``factory`` is the factory which will create the
    content (usually the content class itself), the second argument is
    the content interface (e.g. ``IFoo`` *not*
    ``repoze.lemonade.interfaces.IContent``).  If the content
    interface is later used via ``create_content``, the factory will
    be used to create the content.  Here's a sample test registration
    and usage (the body of a ``unittest.TestCase`` method)::

      from repoze.lemonade.testing import registerContentFactory
      from repoze.lemonade.content import create_content
      from zope.interface import Interface
      class IFoo(Interface):
          pass
      
      class Foo:
          def __init__(self, arg):
              self.arg = arg
      
      registerContentFactory(Foo, IFoo)
      newfoo = create_content(IFoo, 1)
      self.failUnless(newfoo.__class__ is Foo)
      self.assertEqual(newfoo.arg, 1)
    """
    sm = getSiteManager()
    sm.registerAdapter(lambda *arg: factory, (iface,), IContentFactory)
    
    
