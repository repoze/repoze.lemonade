from pkg_resources import EntryPoint
import transaction
from repoze.lemonade.interfaces import IEvolutionManager
from zope.interface import implements

class ZODBEvolutionManager:
    key = 'repoze.lemonade.evolve'
    transaction = transaction
    implements(IEvolutionManager)
    def __init__(self, context, evolve_packagename, sw_version):
        self.context = context
        self.package_name = evolve_packagename
        self.sw_version = sw_version

    @property
    def root(self):
        return self.context._p_jar.root()

    def get_sw_version(self):
        return self.sw_version

    def get_db_version(self):
        registry = self.root.setdefault(self.key, {})
        db_version = registry.get(self.package_name)
        if db_version is None:
            self.transaction.begin()
            self._set_db_version(self.sw_version)
            self.transaction.commit()
            db_version = self.sw_version
        return db_version

    def evolve_to(self, version):
        scriptname = '%s.evolve%s' % (self.package_name, version)
        evmodule = EntryPoint.parse('x=%s' % scriptname).load(False)
        self.transaction.begin()
        evmodule.evolve(self.context)
        self._set_db_version(version)
        self.transaction.commit()

    def _set_db_version(self, version):
        registry = self.root.setdefault(self.key, {})
        db_version = registry[self.package_name] = version
        self.root[self.key] = registry

def evolve_to_latest(manager):
    db_version = manager.get_db_version()
    sw_version = manager.get_sw_version()
    if not isinstance(sw_version, int):
        raise ValueError('software version %s is not an integer' %
                         sw_version)
    if not isinstance(db_version, int):
        raise ValueError('database version %s is not an integer' %
                         db_version)
    if db_version < sw_version:
        for version in range(db_version+1, sw_version+1):
            manager.evolve_to(version)
        return version
    return db_version
