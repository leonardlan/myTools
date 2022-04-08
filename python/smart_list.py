'''My list class with filtering, counting, and sorting.'''

from collections import Counter


def _get_attr(item, key):
    '''Get value from key in item. Can be attribute or square bracket ([]) key.'''
    if hasattr(item, key):
        return getattr(item, key)
    # Try square bracket get.
    try:
        return item[key]
    except:
        pass
    raise ValueError('Could not get key "{}" in item {}'.format(key, item))


class SmartList(list):
    '''List with filtering and counting by attribute.'''

    max_repr_chars = 50

    def __init__(self, *args):
        if isinstance(args, list):
            if len(args) > 1:
                super(SmartList, self).__init__(args)
            elif len(args) == 1:
                super(SmartList, self).__init__(args[0])
        super(SmartList, self).__init__(args)

    def __repr__(self):
        '''If too many characters, print length and type.'''
        rep = 'SmartList({})'.format(super(SmartList, self).__repr__())
        if len(rep) > self.max_repr_chars > 0:
            return 'SmartList({} {})'.format(len(self), self[0].__class__.__name__)
        return rep

    @property
    def types(self):
        '''Unique list of all types in list.'''
        return list(set([type(item) for item in self]))

    @property
    def keys(self):
        '''Unique list of all keys in list.'''
        keys = set()
        for item in self:
            if isinstance(item, dict):
                keys.update(item.keys())
        return list(keys)

    def attr(self, attr):
        '''Returns list of attribute values.'''
        return [_get_attr(item, attr) for item in self]

    def attrs(self, attrs):
        '''Returns lists of attribute values. Can be used to print table.'''
        res = []
        for item in self:
            res.append([_get_attr(item, attr) for attr in attrs])
        return res

    def attr_counter(self, attr):
        '''Returns counter of attribute.'''
        return Counter(_get_attr(item, attr) for item in self)

    def min(self, attr):
        '''Minimum of attribute values.'''
        return min(self.attr(attr))

    def max(self, attr):
        '''Maximum of attribute values.'''
        return max(self.attr(attr))

    def filter(self, **kwargs):
        '''Returns new SmartList instance filtered by attributes/values using an AND operation.
        '''
        new_list = SmartList()
        for item in self:
            for key, val in kwargs.iteritems():
                if _get_attr(item, key) != val:
                    break
            else:
                new_list.append(item)
        return new_list
