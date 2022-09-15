'''My custom wrappers here.'''

import traceback

from functools import wraps


def handle_list(*main_args, **main_kwargs):
    '''If first arg is a list, run function call on each item and return list. Normal otherwise.

    Will not return result(s) from function call if kwarg return_result is False. Defaults to True.
    '''
    def _handle_list(func):
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

                # Return results or not.
                if return_result:
                    return results
                return

            # Just a regular call.
            res = func(*args, **kwargs)
            if return_result:
                return res
        return wrapper

    # Set return_result.
    return_result = main_kwargs.get('return_result', True)

    # If the decorator is @handle_list,
    # main_args is (<function square>,) and main_kwargs is {}.
    # If the decorator is @handle_list(return_result=False),
    # main_args is () and main_kwargs is {'return_result': False}.
    if len(main_args) == 1 and callable(main_args[0]):
        return _handle_list(main_args[0])
    else:
        return _handle_list


@handle_list
def square(num):
    '''Example function for handle_list wrapper. Return number squared.

    >>> square(3)
    9
    >>> square([4, 5, 6])
    [16, 25, 36]
    '''
    return num * num


@handle_list(return_result=False)
def print_square(num):
    '''Same as square(), but prints instead of returning. Tests return_result.

    >>> print_square(3)
    The square of 3 is 9
    >>> print_square([4, 5, 6])
    The square of 4 is 16
    The square of 5 is 25
    The square of 6 is 36
    '''
    squared = square(num)
    print('The square of {} is {}'.format(num, squared))
