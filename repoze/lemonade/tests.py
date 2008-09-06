import unittest

class FolderTests(unittest.TestCase):
    def setUp(self):
        self._cleanup()

    def tearDown(self):
        self._cleanup()

    def _cleanup(self):
        from zope.testing.cleanup import cleanUp
        cleanUp()

    def _getTargetClass(self):
        from repoze.lemonade.folder import Folder
        return Folder

    def _makeOne(self, data=None):
        klass = self._getTargetClass()
        return klass(data)

    def _registerEventListener(self, listener, iface):
        import zope.component
        gsm = zope.component.getGlobalSiteManager()
        gsm.registerHandler(listener, (iface,))

    def test_keys(self):
        folder = self._makeOne({'a':1, 'b':2})
        self.assertEqual(sorted(list(folder.keys())), ['a', 'b'])

    def test__iter__(self):
        folder = self._makeOne({'a':1, 'b':2})
        self.assertEqual(sorted(list(folder.__iter__())), ['a', 'b'])

    def test_values(self):
        folder = self._makeOne({'a':1, 'b':2})
        self.assertEqual(sorted(list(folder.values())), [1, 2])

    def test_items(self):
        folder = self._makeOne({'a':1, 'b':2})
        self.assertEqual(sorted(list(folder.items())), [('a', 1), ('b', 2)])

    def test___nonzero__(self):
        folder = self._makeOne()
        self.failUnless(folder)

    def test___setitem__nonstring(self):
        folder = self._makeOne()
        self.assertRaises(TypeError, folder.__setitem__, None)
        
    def test___setitem__8bitstring(self):
        folder = self._makeOne()
        self.assertRaises(TypeError, folder.__setitem__, '\xff')

    def test___setitem__empty(self):
        folder = self._makeOne()
        self.assertRaises(TypeError, folder.__setitem__, '')

    def test___setitem__(self):
        from repoze.lemonade.interfaces import IObjectEvent
        from repoze.lemonade.interfaces import IObjectAddedEvent
        events = []
        def listener(event):
            events.append(event)
        self._registerEventListener(listener, IObjectEvent)
        dummy = DummyModel()
        folder = self._makeOne()
        folder['a'] = dummy
        self.assertEqual(len(events), 1)
        self.failUnless(IObjectAddedEvent.providedBy(events[0]))
        self.assertEqual(events[0].object, dummy)
        self.assertEqual(events[0].parent, folder)
        self.assertEqual(events[0].name, 'a')

    def test___setitem__exists(self):
        from repoze.lemonade.interfaces import IObjectEvent
        from repoze.lemonade.interfaces import IObjectRemovedEvent
        from repoze.lemonade.interfaces import IObjectAddedEvent
        events = []
        def listener(event):
            events.append(event)
        self._registerEventListener(listener, IObjectEvent)
        dummy1 = DummyModel()
        dummy1.__parent__ = None
        dummy1.__name__ = None
        dummy2 = DummyModel()
        folder = self._makeOne({'a':dummy1})
        folder.__setitem__('a', dummy2)
        self.assertEqual(len(events), 2)
        self.failUnless(IObjectRemovedEvent.providedBy(events[0]))
        self.failUnless(IObjectAddedEvent.providedBy(events[1]))
        self.assertEqual(events[0].object, dummy1)
        self.assertEqual(events[0].parent, folder)
        self.assertEqual(events[0].name, 'a')
        self.assertEqual(events[1].object, dummy2)
        self.assertEqual(events[1].parent, folder)
        self.assertEqual(events[1].name, 'a')

    def test___delitem__(self):
        from repoze.lemonade.interfaces import IObjectEvent
        from repoze.lemonade.interfaces import IObjectRemovedEvent
        events = []
        def listener(event):
            events.append(event)
        self._registerEventListener(listener, IObjectEvent)
        dummy = DummyModel()
        dummy.__parent__ = None
        dummy.__name__ = None
        folder = self._makeOne({'a':dummy})
        del folder['a']
        self.assertEqual(len(events), 1)
        self.failUnless(IObjectRemovedEvent.providedBy(events[0]))
        self.assertEqual(events[0].object, dummy)
        self.assertEqual(events[0].parent, folder)
        self.assertEqual(events[0].name, 'a')
        self.failIf(hasattr(dummy, '__parent__'))
        self.failIf(hasattr(dummy, '__name__'))

class DummyModel:
    pass

