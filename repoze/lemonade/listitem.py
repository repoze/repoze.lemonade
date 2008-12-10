from zope.component import getSiteManager

def get_listitems(iface):
    sm = getSiteManager()
    items = []

    for utility in sm.registeredUtilities():
        if utility.provided is iface:
            D = {}
            D['name'] = utility.name
            info = utility.info or {}
            D['title'] = info.get('title')
            D['description'] = info.get('description')
            D['sort_key'] = info.get('sort_key')
            D['component'] = utility.component
            items.append(D)

    items.sort(lambda x, y: cmp(x['sort_key'], y['sort_key']))
    return items
    
