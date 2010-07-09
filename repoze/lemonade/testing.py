from zope.component import getSiteManager

from repoze.lemonade.interfaces import IContentFactory

def registerContentFactory(factory, iface):
    """ Registers a lemonade ``IContentFactory`` (so it can be later
    looked up by ``create_content`` ``get_content_type``, or
    ``get_content_types``).  The first argument, ``factory`` is the
    factory which will create the content (usually the content class
    itself), the second argument is the content interface
    (e.g. ``IFoo`` *not* ``repoze.lemonade.interfaces.IContent``).

    Here's a sample test registration and usage (the body of a
    ``unittest.TestCase`` method) which demonstrates that if a content
    interface is later used by ``create_content``, the factory will be
    used to create the content and if a piece of content is used by
    ``get_content_type``, the factory will be used to locate the
    type interface::

      from repoze.lemonade.testing import registerContentFactory
      from repoze.lemonade.content import create_content
      from repoze.lemonade.content import get_content_type

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
      ct = get_content_type(newfoo)
      self.assertEqual(ct, IFoo)
    
    """
    sm = getSiteManager()
    sm.registerAdapter(lambda *arg: factory, (iface,), IContentFactory)
    
    
def registerListItem(provides, component, name, title=None,
                     description=None, sort_key=0):
    """ Register a lemonade 'list item'.  A list item is a utility
    registered for the ``provides`` interface and the ``name`` name,
    using the ``component`` as the utility implementation.  It
    includes the the name, the title, the description, and the
    sort_key as metadata in the component registry for later
    consumption by ``repoze.lemonade.listitem.get_listitems``.  You
    will want to use this testing API when you need to emulate the
    result of some ``lemonade:listitem`` ZCML registration.  For example::

      from zope.interface import Interface
      class IFoo(Interface):
          pass
      def foo_one():
          pass
      from repoze.lemonade.testing import registerListItem
      registerListItem(IFoo, foo_one, 'foo_one')

      from repoze.lemonade.listitem import get_listitems
      items = get_listitems(IFoo)
      self.assertEqua(len(items), 1)
      self.assertEqual(items[0]['name'], 'foo_one')
      self.assertEqual(items[0]['component'], foo_one)
    """
    sm = getSiteManager()
    info = {'title':title, 'description':description, 'sort_key':sort_key}
    sm.registerUtility(component, provides, name, info)
