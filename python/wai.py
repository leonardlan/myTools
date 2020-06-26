'''What am I? Call wai(anything) and find out what it is.'''
import inspect
import math
import os
import re
import sys
import time

from pprint import pprint, pformat
from types import ModuleType

from colors import (BLUE, BRIGHT, CYAN, DIM, GREEN, NORMAL, MAGENTA, RED, RESET, RESET_ALL, YELLOW,
                    bright_blue)
from lancore import human_int, var_name
from my_settings import MAX_LINES


IGNORED_ATTRIBUTES = ['__builtins__', '__globals__', 'func_globals']
FILE_TYPE_TO_EXTENSION = {
    'EXR image': 'exr',
    'Katana file': 'katana',
    'Log file': 'log',
    'Markdown file': 'md',
    'Maya ascii file': 'ma',
    'Maya binary file': 'mb',
    'Nuke script': 'nk',
    'JSON file': 'json',
    'Python file': 'py',
}
TYPE_TO_REGEX = {
    'E-mail': r'^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,5})$',
    'Whole number': r'^\d+$',
    'Negative int': r'^-\d+$',
    'Negative float': r'^-\d+$',
    'Decimal number (float)': r'^\d*\.\d+$',
    'IP Address': r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',
    'MAC Address': r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$',
    'UUID': r'[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}',
}


def wai(*things, **kwargs):
    '''What am I? Feed me anything. I'll tell you what it is.'''
    for thing in things:
        _wai(thing, **kwargs)


def _wai_text(str_, typ):
    '''What is this text? Can be unicode or str.'''
    if str_:
        if os.path.exists(str_):
            # It's a file path.
            if os.path.isfile(str_):
                for file_type, extension in FILE_TYPE_TO_EXTENSION.iteritems():
                    if str_.endswith(extension):
                        print file_type
                        break
                else:
                    print 'file path'
            else:
                print 'directory'
        else:
            # Match by regex of what we know.
            for type_, regex in TYPE_TO_REGEX.iteritems():
                if re.match(regex, str_):
                    print type_
                    break
            else:
                print 'Just a %s:' % typ.__name__, str_
    else:
        print 'Empty %s: ''' % typ.__name__


def _wai_number(num, typ):
    '''What is this number? Can be int or float.'''
    if num >= 946702800:  # Epoch date
        print 'Epoch time'
        print time.strftime('%Z - %a %Y-%m-%d, %I:%M:%S %p', time.localtime(num))
    elif typ == int:
        if num >= 16:
            # Check if it's a power of 2
            log = math.log(num, 2)
            if log.is_integer():
                print '%i = 2^%i' % (num, int(log))
                return
        print 'Just an int:', human_int(num)
    elif typ == float:
        print 'Just a float:', num


def _wai_list(list_, typ):
    '''What is this list/tuple?'''
    if list_:
        print BLUE + '%s of %s %s%s' % (
            typ.__name__.title(),
            human_int(len(list_)),
            get_types(list_),
            's' if len(list_) > 1 else ''
        )
        print NORMAL + GREEN + '%s[0]: ' % var_name(list_),
        wai(list_[0])
        _print_parent_types(type(list_[0]))
    else:
        print DIM + 'Empty %s: %s' % (typ.__name__, str(list_)) + RESET_ALL


def _wai_dict(dict_):
    '''What is this dict?'''
    if not dict_:
        print DIM + 'Empty dict: {}' + RESET_ALL
        return

    keys = dict_.keys()
    print BLUE + 'Just a dict of %i {%s: %s}' % (
        len(dict_), get_types(keys), get_types(dict_.values()))

    keys_print = pformat(sorted(keys)).split('\n')
    print 'Keys: ' + RESET_ALL + GREEN + '\n'.join(keys_print[:50])
    if len(keys_print) > MAX_LINES:
        print '...'

    # Print dict with least number of depth that's less than MAX_LINES.
    depth = 1
    previous_output = ''
    while True:
        output = pformat(dict_, depth=depth)
        if output.count('\n') > MAX_LINES:
            break

        # Check if everything expanded.
        if output == previous_output:
            break
        previous_output = output
        depth += 1
    if previous_output and depth > 2:
        print bright_blue('Dict:') + GREEN
        print previous_output


def _brighten_it_up(func):
    '''Brighten up the output.'''
    def wrapper(*args, **kwargs):
        '''Wrapper func.'''
        sys.stdout.write(BRIGHT)
        res = func(*args, **kwargs)
        sys.stdout.write(RESET_ALL)
        return res
    return wrapper


@_brighten_it_up
def _wai(thing, ignore_private=False, ignore_attrs=[], call=False, skip_callable=False,
         skip_module=True, skip_known=False):
    '''What Am I? Prints type and attributes of object thing.

    :param thing object: Anything and everything. That's what we're here to find out. :)
    :param ignore_private bool: Ignores attributes starting with underscore.
    :param ignore_attrs list: Attributes to ignore.
    :param call bool: Calls attributes that are functions and thing itself if it is callable.
    :param skip_callable bool: Doesn't print callable attributes.
    :param skip_module bool: Skips module attributes.
    :param skip_known bool: If True, prints every attribute even if we know what it is.
    '''
    typ = type(thing)

    if not skip_known:
        # Let's see if we know what it is first.
        if thing is None:
            print "It's just None!"
            return
        elif typ in (str, unicode):
            return _wai_text(thing, typ)
        elif typ in (int, float):
            return _wai_number(thing, typ)
        elif typ == dict:
            return _wai_dict(thing)

        from collections import defaultdict, Counter, OrderedDict
        if typ in (defaultdict, Counter, OrderedDict):
            print BLUE + '%s with %i key%s: %s' % (
                typ.__name__.title(), len(thing), 's' if len(thing) > 1 else '', thing.keys())
            return
        elif typ in (list, tuple):
            return _wai_list(thing, typ)

    if callable(thing):
        print _func_name_args_kwargs(thing)
        if thing.__doc__:
            print thing.__doc__

    # So we don't know what it is. Let's print everything we can find about it.
    thing_name = getattr(thing, '__name__', '')
    call_count = private_count = total = 0
    ignore_attrs += IGNORED_ATTRIBUTES
    for attr in dir(thing):
        if attr in ignore_attrs:
            continue
        if attr.startswith('_'):
            private_count += 1
            if ignore_private:
                continue
        total += 1
        try:
            res = getattr(thing, attr)
        except Exception, err:
            print RED + str(err)
            continue

        # Skip if module
        if isinstance(res, ModuleType) and skip_module:
            continue

        # Skip if callable
        is_callable = callable(res)
        long_name = '%s.%s' % (thing_name, attr)
        if is_callable and skip_callable:
            continue
        elif is_callable:
            # Print *args, **kwargs
            print _func_name_args_kwargs(res),
            call_count += 1
            if call:
                _call(res)
            else:
                print getattr(res, '__doc__')
        else:
            print BLUE + '%s:' % long_name + GREEN,
            _print(res)
    if call and callable(thing):
        _call(thing)
    sys.stdout.write(CYAN)
    if not skip_callable:
        print 'Callable: %i,' % call_count,
    print 'Uncallable: %i' % (total - call_count)
    print 'Private: %i, Public: %i' % (private_count, total - private_count)
    print 'Total: %i' % total

    _print_parent_types(typ)


def _func_name_args_kwargs(func):
    varnames_str = ''
    code = getattr(func, '__code__', None)
    if code:
        co_argcount = getattr(code, 'co_argcount', None)
        co_varnames = getattr(code, 'co_varnames', None)
        if co_argcount and co_varnames:
            try:
                varnames = list(co_varnames)[0:co_argcount]
            except TypeError:
                print 'Could not get func args for', co_varnames
                return varnames_str
            defaults = getattr(func, '__defaults__', [])
            if defaults:
                for i, default in enumerate(defaults):
                    index = len(varnames) - len(defaults) + i
                    varnames[index] = MAGENTA + varnames[index] + BLUE + '=' + YELLOW + \
                        str(default) + BLUE
            varnames_str = ', '.join(varnames)
    func_name = func.__name__ if hasattr(func, '__name__') else str(func)
    return BLUE + '%s(%s):' % (func_name, varnames_str) + GREEN


def _print_parent_types(typ):
    '''Print types of all parent classes.'''
    import inspect
    print typ
    print CYAN + 'Parents:' + GREEN, ' -> '.join([t.__name__ for t in inspect.getmro(typ)[1:]])
    print CYAN + 'Type:' + GREEN, typ.__name__, RESET


def _call(func):
    try:
        res = func()
        _print(res)
    except Exception, err:
        print RED, err


def _print(to_print):
    if isinstance(to_print, basestring):
        print to_print
    else:
        pprint(to_print)


def get_types(items):
    '''String of unique types in items.

    >>> get_types(['a', 'b', 'c'])
    'str'
    >>> get_types(['apple', 'banana', u'peach', 2])
    'int, unicode, str'
    '''
    found_types = set()
    for item in items:
        found_types.add(type(item))
    return ', '.join([typ.__name__ for typ in found_types])


def call_gets(obj):
    '''Calls all methods of object starting with 'get' and requiring no args.'''
    called_count = 0
    for attr_name in dir(obj):
        attr = getattr(obj, attr_name)
        if callable(attr) and attr_name.startswith('get'):
            try:
                args = inspect.getargspec(attr)[0]
            except:
                print 'Could not get args of callable %s' % attr_name
                continue
            if len(args) == 1:  # No args other than 'self'.
                print '%s: %s' % (attr_name, attr())
                called_count += 1
    print 'Called %i get function(s)' % called_count
