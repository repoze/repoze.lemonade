import unittest

class EvolveTests(unittest.TestCase):
    def _callFUT(self, *arg, **kw):
        from repoze.lemonade.evolution import evolve_to_latest
        return evolve_to_latest(*arg, **kw)

    def test_success_no_db_version(self):
        root = {}
        ob = DummyPersistent(root)
        t = DummyTransaction()
        from repoze.lemonade.tests.fixtureapp import evolve
        evolve.__version__ = 1
        v = self._callFUT(evolve, ob, t)
        self.assertEqual(v, 1)
        self.assertEqual(ob.evolved, None)
        self.assertEqual(t.committed, 1)
        reg = root['repoze.lemonade.evolve']
        self.assertEqual(reg['repoze.lemonade.tests.fixtureapp.evolve'], 1)

    def test_success_with_db_version(self):
        root = {'repoze.lemonade.evolve':
                {'repoze.lemonade.tests.fixtureapp.evolve':1}}
        ob = DummyPersistent(root)
        t = DummyTransaction()
        from repoze.lemonade.tests.fixtureapp import evolve
        evolve.__version__ = 2
        v = self._callFUT(evolve, ob, t)
        self.assertEqual(v, 2)
        self.assertEqual(ob.evolved, 2)
        self.assertEqual(t.committed, 1)
        reg = root['repoze.lemonade.evolve']
        self.assertEqual(reg['repoze.lemonade.tests.fixtureapp.evolve'], 2)

    def test_evolve_error(self):
        root = {'repoze.lemonade.evolve':
                {'repoze.lemonade.tests.fixtureapp.evolve':0}}
        ob = DummyPersistent(root)
        t = DummyTransaction()
        from repoze.lemonade.tests.fixtureapp import evolve
        evolve.__version__ = 3
        self.assertRaises(ValueError, self._callFUT, evolve, ob, t)
        self.assertEqual(ob.evolved, 2)
        self.assertEqual(t.committed, 2)
        reg = root['repoze.lemonade.evolve']
        self.assertEqual(reg['repoze.lemonade.tests.fixtureapp.evolve'], 2)

    def test_noevolve(self):
        root = {'repoze.lemonade.evolve':
                {'repoze.lemonade.tests.fixtureapp.evolve':1}}
        ob = DummyPersistent(root)
        t = DummyTransaction()
        from repoze.lemonade.tests.fixtureapp import evolve
        evolve.__version__ = 1
        v = self._callFUT(evolve, ob, t)
        self.assertEqual(v, 1)
        self.assertEqual(ob.evolved, None)
        self.assertEqual(t.committed, 0)
        reg = root['repoze.lemonade.evolve']
        self.assertEqual(reg['repoze.lemonade.tests.fixtureapp.evolve'], 1)

class Dummy(object):
    pass

class DummyPersistent(object):
    evolved = None
    def __init__(self, root):
        self._p_jar = Dummy()
        self._p_jar.root = lambda *arg: root
        self.error = False
        
class DummyTransaction(object):
    committed = 0
    begun = 0
    def commit(self):
        self.committed = self.committed + 1

    def begin(self):
        self.begun = self.begun + 1
        
        
        
