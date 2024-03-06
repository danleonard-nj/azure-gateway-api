

def first(items, func=None):
    for item in items:
        if func is None:
            return item
        if func(item) is True:
            return item
