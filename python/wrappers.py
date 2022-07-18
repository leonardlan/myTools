'''My custom wrappers here.'''

import traceback

from functools import wraps


def handle_list(func):
    '''If first arg is a list, run function call on each item and return list. Normal otherwise.'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        '''Wrapper func.'''
        if args and isinstance(args[0], list):
            args = list(args)  # Cast to list because defaults to tuple.
            # Handle first arg is list.
            results = []
            first_arg_list = args[0]
            for arg in first_arg_list:
                args[0] = arg
                try:
                    res = func(*args, **kwargs)
                except Exception:
                    print(traceback.format_exc())
                    raise RuntimeError('Function call {}({}...) failed'.format(func.__name__, arg))
                else:
                    results.append(res)
            return results

        # Just a regular call.
        return func(*args, **kwargs)
    return wrapper


@handle_list
def square(num):
    '''Example function for handle_list wrapper. Return number squared.

    >>> square(3)
    9
    >>> square([4, 5, 6])
    [16, 25, 36]
    '''
    return num * num
