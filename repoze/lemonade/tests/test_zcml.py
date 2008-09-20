import unittest
from zope.component.testing import PlacelessSetup

class TestContentDirective(unittest.TestCase, PlacelessSetup):
    def setUp(self):
        PlacelessSetup.setUp(self)

    def tearDown(self):
        PlacelessSetup.tearDown(self)

    def _callFUT(self, *arg, **kw):
        from repoze.lemonade.zcml import content
        return content(*arg, **kw)

    def test_it(self):
        class Foo:
            def __init__(self, **kw):
                self.kw = kw

        from zope.interface import Interface
        from repoze.lemonade.interfaces import IContentType
        from repoze.lemonade.interfaces import IContentFactory

        class IFoo(Interface):
            pass

        context = DummyContext()

        from zope.component.interface import provideInterface
        from zope.component.zcml import handler

        self._callFUT(context, Foo, IFoo)

        self.assertEqual(len(context.actions), 2)
        provide = context.actions[0]
        self.assertEqual(provide['discriminator'],
                         ('content', IFoo, IContentType))
        self.assertEqual(provide['callable'], provideInterface)
        self.assertEqual(provide['args'], ('', IFoo, IContentType))

        register = context.actions[1]
        self.assertEqual(register['discriminator'],
                         ('content', Foo, IFoo, IContentFactory))
        self.assertEqual(register['callable'], handler)
        self.assertEqual(register['args'][0], 'registerAdapter')
        self.assertEqual(register['args'][1].factory, Foo)
        self.assertEqual(register['args'][2], (IFoo,))
        self.assertEqual(register['args'][3], IContentFactory)
        self.assertEqual(register['args'][4], '')
        self.assertEqual(register['args'][5], context.info)

class TestContent(unittest.TestCase, PlacelessSetup):
    def setUp(self):
        PlacelessSetup.setUp(self)

    def tearDown(self):
        PlacelessSetup.tearDown(self)

    def get_context(self):
        import repoze.lemonade.tests.fixtureapp as package
        from zope.configuration import xmlconfig
        from zope.configuration import config
        context = config.ConfigurationMachine()
        xmlconfig.registerCommonDirectives(context)
        context.package = package
        xmlconfig.include(context, 'configure.zcml', package)
        context.execute_actions(clear=False)
        return context

    def test_registry_actions_can_be_pickled_and_unpickled(self):
        context = self.get_context()
        actions = context.actions
        import cPickle
        dumped = cPickle.dumps(actions, -1)
        new = cPickle.loads(dumped)
        self.assertEqual(len(actions), len(new))

    def test_create_content(self):
        from repoze.lemonade.tests.fixtureapp import content
        context = self.get_context()
        from repoze.lemonade.content import create_content
        ob = create_content(content.IFoo, 'arg1', kw1='kw1', kw2='kw2')
        self.failUnless(isinstance(ob, content.Foo))
        self.assertEqual(ob.arg, ('arg1',))
        self.assertEqual(ob.kw, {'kw1':'kw1', 'kw2':'kw2'})

    def test_fail_create_content(self):
        context = self.get_context()
        from repoze.lemonade.content import create_content
        from zope.interface import Interface
        class IBar(Interface):
            pass
        from zope.component import ComponentLookupError
        self.assertRaises(ComponentLookupError, create_content, IBar)

    def test_get_content_types(self):
        from repoze.lemonade.tests.fixtureapp import content
        context = self.get_context()
        from repoze.lemonade.content import get_content_types
        types = get_content_types()
        self.assertEqual(len(types), 1)
        foo = types[0]
        self.assertEqual(foo, content.IFoo)

class DummyContext:
    info = None
    def __init__(self):
        self.actions = []

    def action(self, discriminator, callable, args):
        self.actions.append(
            {'discriminator':discriminator,
             'callable':callable,
             'args':args}
            )
