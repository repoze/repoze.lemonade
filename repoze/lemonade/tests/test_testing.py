import unittest
from zope.testing.cleanup import cleanUp

class TestRegisterContentFactory(unittest.TestCase):
    def setUp(self):
        cleanUp()

    def tearDown(self):
        cleanUp()
        
    def _callFUT(self, factory, iface):
        from repoze.lemonade.testing import registerContentFactory
        return registerContentFactory(factory, iface)

    def test_it(self):
        from zope.interface import Interface
        from zope.interface import implements
        from zope.component import getGlobalSiteManager
        from repoze.lemonade.interfaces import IContentFactory

        class IFoo(Interface):
            pass
        class FooContent(object):
            implements(IFoo)
        foo = FooContent()

        def factory():
            """"""

        self._callFUT(factory, IFoo)
        gsm = getGlobalSiteManager()

        self.assertEqual(gsm.getAdapter(foo, IContentFactory), factory)

    def test_functional_with_create_content(self):
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
        
    def test_functional_with_get_content_types(self):
        from repoze.lemonade.testing import registerContentFactory
        from repoze.lemonade.content import get_content_types
        from zope.interface import Interface
        class IFoo(Interface):
            pass
        class Foo:
            def __init__(self, arg):
                self.arg = arg
        registerContentFactory(Foo, IFoo)
        self.assertEqual(get_content_types(), [IFoo])
        
        
                         
        
