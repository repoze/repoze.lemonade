import unittest
from zope.testing.cleanup import cleanUp

class TestGetListitems(unittest.TestCase):
    def setUp(self):
        cleanUp()

    def tearDown(self):
        cleanUp()

    def _callFUT(self, iface):
        from repoze.lemonade.listitem import get_listitems
        return get_listitems(iface)

    def _setupListItems(self):
        import zope.component
        gsm = zope.component.getGlobalSiteManager()
        gsm.registerUtility(component, IFoo, 'listitem1',
                            {'title':'title1', 'description':'description1',
                             'sort_key':10})
        gsm.registerUtility(component, IFoo, 'listitem2',
                            {'title':'title2', 'description':'description2',
                             'sort_key':20})

    def test_get_listitems_some_registered(self):
        self._setupListItems()
        items = self._callFUT(IFoo)
        self.assertEqual(len(items), 2)

        self.assertEqual(items[0]['name'], 'listitem1')
        self.assertEqual(items[0]['title'], 'title1')
        self.assertEqual(items[0]['description'],'description1')
        self.assertEqual(items[0]['sort_key'], 10)
        self.assertEqual(items[0]['component'], component)

        self.assertEqual(items[1]['name'], 'listitem2')
        self.assertEqual(items[1]['title'], 'title2')
        self.assertEqual(items[1]['description'],'description2')
        self.assertEqual(items[1]['sort_key'], 20)
        self.assertEqual(items[1]['component'], component)

    def test_get_listitems_none_registered(self):
        items = self._callFUT(IFoo)
        self.assertEqual(len(items), 0)

from zope.interface import Interface
class IFoo(Interface):
    pass

def component(): pass
