import unittest
from zope.component.testing import PlacelessSetup

class TestContent(unittest.TestCase, PlacelessSetup):
    def setUp(self):
        PlacelessSetup.setUp(self)

    def tearDown(self):
        PlacelessSetup.tearDown(self)

    def _setupContentTypes(self):
        import zope.component
        gsm = zope.component.getGlobalSiteManager()
        from repoze.lemonade.tests.fixtureapp.content import IFoo
        from repoze.lemonade.tests.fixtureapp.content import Foo
        from repoze.lemonade.tests.fixtureapp.content import IBar
        from repoze.lemonade.tests.fixtureapp.content import Bar
        from zope.component.interface import provideInterface
        from repoze.lemonade.interfaces import IContentType
        from repoze.lemonade.interfaces import IContentFactory
        from repoze.lemonade.zcml import HammerFactoryFactory
        provideInterface('', IFoo, IContentType)
        gsm.registerAdapter(HammerFactoryFactory(Foo), (IFoo,), IContentFactory)
        provideInterface('', IBar, IContentType)
        gsm.registerAdapter(HammerFactoryFactory(Bar), (IBar,), IContentFactory)

    def test_create_content(self):
        self._setupContentTypes()
        from repoze.lemonade.tests.fixtureapp import content
        from repoze.lemonade.content import create_content
        ob = create_content(content.IFoo, 'arg1', kw1='kw1', kw2='kw2')
        self.failUnless(isinstance(ob, content.Foo))
        self.assertEqual(ob.arg, ('arg1',))
        self.assertEqual(ob.kw, {'kw1':'kw1', 'kw2':'kw2'})

    def test_fail_create_content(self):
        self._setupContentTypes()
        from repoze.lemonade.content import create_content
        from zope.interface import Interface
        class IBar(Interface):
            pass
        from zope.component import ComponentLookupError
        self.assertRaises(ComponentLookupError, create_content, IBar)

    def test_get_content_types_nocontext(self):
        self._setupContentTypes()
        from repoze.lemonade.tests.fixtureapp import content
        from repoze.lemonade.content import get_content_types
        types = get_content_types()
        self.assertEqual(len(types), 2)
        self.assertEqual(types, [content.IFoo, content.IBar])

    def test_get_content_types_context(self):
        self._setupContentTypes()
        from repoze.lemonade.tests.fixtureapp import content
        from repoze.lemonade.content import get_content_types
        from zope.interface import implements
        class Fred:
            implements(content.IBar)
        fred = Fred()
        types = get_content_types(fred)
        self.assertEqual(len(types), 1)
        self.assertEqual(types, [content.IBar])
        
