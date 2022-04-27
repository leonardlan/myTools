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
        if len(args) > 1:
            args = (list(args),)
        elif len(args) == 1 and not isinstance(args[0], list):
            args = (list(args),)
        super(SmartList, self).__init__(*args)

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
    def all_same_type(self):
        '''True if all items are same type.'''
        return len(self.types) == 1

    @property
    def keys(self):
        '''Unique list of all keys in list.'''
        keys = set()
        for item in self:
            if isinstance(item, dict):
                keys.update(item.keys())
        return list(keys)

    def attr(self, attr, ignored_values=None, types=None):
        '''Returns list of attribute values.'''
        values = []
        for item in self:
            val = _get_attr(item, attr)
            if types:
                if isinstance(val, types):
                    values.append(val)
            elif not ignored_values or val not in ignored_values:
                values.append(val)
        return values

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
        '''Minimum of attribute values of type int/float.'''
        return min(self.attr(attr, types=(int, float)))

    def average(self, attr):
        '''Average of attribute values as float. Only sums from ints, floats and longs.'''
        values = self.attr(attr, types=(int, float))
        if not values:
            return
        return float(sum(values)) / len(values)

    def max(self, attr):
        '''Maximum of attribute values of type int/float.'''
        return max(self.attr(attr, types=(int, float)))

    def filter(self, **kwargs):
        '''Returns new SmartList instance filtered by attributes/values using an AND operation.
        '''
        new_list = SmartList()
        for item in self:
            for key, val in kwargs.items():
                if _get_attr(item, key) != val:
                    break
            else:
                new_list.append(item)
        return new_list
