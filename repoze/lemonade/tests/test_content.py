import unittest
from zope.testing.cleanup import cleanUp

class TestContent(unittest.TestCase):
    def setUp(self):
        cleanUp()

    def tearDown(self):
        cleanUp()

    def _setupContentTypes(self):
        import zope.component
        gsm = zope.component.getGlobalSiteManager()
        from repoze.lemonade.tests.fixtureapp.content import IFoo
        from repoze.lemonade.tests.fixtureapp.content import Foo
        from repoze.lemonade.tests.fixtureapp.content import IBar
        from repoze.lemonade.tests.fixtureapp.content import Bar
        from repoze.lemonade.interfaces import IContentFactory
        from repoze.lemonade.zcml import HammerFactoryFactory
        gsm.registerAdapter(HammerFactoryFactory(Foo), (IFoo,), IContentFactory)
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
        types =sorted(get_content_types())
        self.assertEqual(len(types), 2)
        self.assertEqual(types, [content.IBar, content.IFoo])

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

    def test_get_content_types_does_caching(self):
        self._setupContentTypes()
        from repoze.lemonade.tests.fixtureapp import content
        from repoze.lemonade.content import get_content_types
        from repoze.lemonade.interfaces import IContentTypeCache
        from zope.interface import implements
        from zope.component import getSiteManager
        class Fred:
            implements(content.IBar)
        fred = Fred()
        get_content_types(fred)
        sm = getSiteManager()
        cache = sm.getUtility(IContentTypeCache)
        self.failUnless(content.IBar in cache)
        
    def test_get_content_type_withcontent(self):
        self._setupContentTypes()
        from repoze.lemonade.tests.fixtureapp import content
        from repoze.lemonade.content import get_content_type
        from zope.interface import implements
        class Fred:
            implements(content.IBar)
        fred = Fred()
        type = get_content_type(fred)
        self.assertEqual(type, content.IBar)

    def test_get_content_type_has_more_than_one_type(self):
        from repoze.lemonade.content import _marker
        self._setupContentTypes()
        from repoze.lemonade.content import get_content_type
        self.assertRaises(ValueError, get_content_type, _marker)

    def test_get_content_type_withcontent_multipletypes(self):
        self._setupContentTypes()
        from repoze.lemonade.tests.fixtureapp import content
        from repoze.lemonade.content import get_content_type
        from zope.interface import implements
        class Fred:
            implements(content.IBar, content.IFoo)
        fred = Fred()
        self.assertRaises(ValueError, get_content_type, Fred)

    def test_get_content_type_withnoncontent(self):
        self._setupContentTypes()
        from repoze.lemonade.content import get_content_type
        class Fred:
            pass
        fred = Fred()
        self.assertRaises(ValueError, get_content_type, Fred)

    def test_iscontent(self):
        from zope.interface import implements
        from repoze.lemonade.interfaces import IContent
        from repoze.lemonade.content import is_content
        class Content:
            implements(IContent)
        content = Content()
        self.failUnless(is_content(content))
        self.failIf(is_content(None))

