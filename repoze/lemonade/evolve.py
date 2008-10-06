from pkg_resources import EntryPoint
import transaction

KEY = 'repoze.lemonade.evolve'

def evolve(package, ob, transaction=transaction):
    # transaction overrideable for unit tests
    package_name = package.__name__
    package_version = getattr(package, '__version__', 0)
    root = ob._p_jar.root()
    registry = root.setdefault(KEY, {})
    db_version = registry.get(package_name)
    if db_version is None:
        transaction.begin()
        db_version = registry[package_name] = package_version
        root[KEY] = registry
        transaction.commit()
    if not isinstance(package_version, int):
        raise ValueError('package __version__ %s is not an integer' %
                         package_version)
    if db_version < package_version:
        for version in range(db_version+1, package_version+1):
            scriptname = '%s.evolve%s' % (package_name, version)
            evmodule = EntryPoint.parse('x=%s' % scriptname).load(False)
            transaction.begin()
            evmodule.evolve(ob)
            registry[package_name] = version
            root[KEY] = registry
            transaction.commit()
        return version
    return db_version
