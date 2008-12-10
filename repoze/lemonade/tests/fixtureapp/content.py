from zope.interface import Interface

class Foo:
    def __init__(self, *arg, **kw):
        self.arg = arg
        self.kw = kw

class IFoo(Interface):
    pass

class Bar:
    def __init__(self, *arg, **kw):
        self.arg = arg
        self.kw = kw

class IBar(Interface):
    pass
    
class IListItem(Interface):
    pass

def listitemcomponent():
    pass

