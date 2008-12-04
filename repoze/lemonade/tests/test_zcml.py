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

    def test_not_an_interface(self):
        from zope.configuration.exceptions import ConfigurationError
        context = DummyContext()
        self.assertRaises(ConfigurationError, self._callFUT, context,None, None)

    def test_it(self):
        class Foo:
            def __init__(self, **kw):
                self.kw = kw

        from zope.interface import Interface
        from repoze.lemonade.interfaces import IContent
        from repoze.lemonade.interfaces import IContentType
        from repoze.lemonade.interfaces import IContentFactory
        from repoze.lemonade.zcml import addbase

        class IFoo(Interface):
            pass

        context = DummyContext()

        from zope.component.interface import provideInterface
        from zope.component.zcml import handler

        self._callFUT(context, Foo, IFoo)

        self.assertEqual(len(context.actions), 3)
        provide = context.actions[0]
        self.assertEqual(provide['discriminator'],
                         ('content', IFoo, IContentType))
        self.assertEqual(provide['callable'], provideInterface)
        self.assertEqual(provide['args'], ('', IFoo, IContentType))

        provide = context.actions[1]
        self.assertEqual(provide['discriminator'],
                         ('content', IFoo, IContent))
        self.assertEqual(provide['callable'], addbase)
        self.assertEqual(provide['args'], (IFoo, IContent))

        register = context.actions[2]
        self.assertEqual(register['discriminator'],
                         ('content', Foo, IFoo, IContentFactory))
        self.assertEqual(register['callable'], handler)
        self.assertEqual(register['args'][0], 'registerAdapter')
        self.assertEqual(register['args'][1].factory, Foo)
        self.assertEqual(register['args'][2], (IFoo,))
        self.assertEqual(register['args'][3], IContentFactory)
        self.assertEqual(register['args'][4], '')
        self.assertEqual(register['args'][5], context.info)

class TestPickling(unittest.TestCase, PlacelessSetup):
    def setUp(self):
        PlacelessSetup.setUp(self)

    def tearDown(self):
        PlacelessSetup.tearDown(self)

    def test_registry_actions_can_be_pickled_and_unpickled(self):
        import repoze.lemonade.tests.fixtureapp as package
        from zope.configuration import xmlconfig
        from zope.configuration import config
        context = config.ConfigurationMachine()
        xmlconfig.registerCommonDirectives(context)
        context.package = package
        xmlconfig.include(context, 'configure.zcml', package)
        context.execute_actions(clear=False)
        actions = context.actions
        import cPickle
        dumped = cPickle.dumps(actions, -1)
        new = cPickle.loads(dumped)
        self.assertEqual(len(actions), len(new))

class TestAddBase(unittest.TestCase):
    def _callFUT(self, I1, I2):
        from repoze.lemonade.zcml import addbase
        return addbase(I1, I2)

    def test_already_in_iro(self):
        from repoze.lemonade.interfaces import IContent
        class IFoo(IContent):
            pass
        result = self._callFUT(IFoo, IContent)
        self.assertEqual(result, False)
        
    def test_not_in_iro(self):
        from zope.interface import Interface
        from repoze.lemonade.interfaces import IContent
        class IFoo(Interface):
            pass
        result = self._callFUT(IFoo, IContent)
        self.assertEqual(result, True)
        self.failUnless(IContent in IFoo.__bases__)
        self.failUnless(IContent in IFoo.__iro__)

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
