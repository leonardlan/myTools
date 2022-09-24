'''My custom wrappers here.'''

import traceback

from functools import wraps


DEFAULT_PRINT_FUNC_CALL = False
DEFAULT_RETURN_RESULT = True


def handle_list(*main_args, **main_kwargs):
    '''Decorator to handle item or list of items as first argument to function call.

    If first arg is a list, run function call on each item and return list. Normal otherwise.

    Special Kwargs:
        print_func_call (bool): Print function call with argument when handling list and if True.
            Defaults to False.
        return_result (bool): Return results from function call as list, if True. None otherwise.
            Defaults to True.

    Returns:
        list or None: List of results from function calls.

    See functions square(num) and print_square(num) before for examples.
    '''
    def _handle_list(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            '''Wrapper func.'''
            if args and isinstance(args[0], list):
                # Handle list.
                args = list(args)  # Cast to list because defaults to tuple.
                # Handle first arg is list.
                results = []
                first_arg_list = args[0]
                for arg in first_arg_list:
                    # Print function call prior to calling.
                    func_call_str = None
                    if print_func_call:
                        func_call_str = _get_func_call_str(func, arg, args, kwargs)
                        print('Calling {}:'.format(func_call_str))

                    # Call function.
                    args[0] = arg
                    try:
                        res = func(*args, **kwargs)
                    except Exception:
                        print(traceback.format_exc())
                        func_call_str = func_call_str or _get_func_call_str(func, arg, args, kwargs)
                        raise RuntimeError('Function call {} failed'.format(func_call_str))
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

    # Set default main_kwargs.
    print_func_call = main_kwargs.get('print_func_call', DEFAULT_PRINT_FUNC_CALL)
    return_result = main_kwargs.get('return_result', DEFAULT_RETURN_RESULT)

    # If the decorator is @handle_list,
    # main_args is (<function square>,) and main_kwargs is {}.
    # If the decorator is @handle_list(return_result=False),
    # main_args is () and main_kwargs is {'return_result': False}.
    if len(main_args) == 1 and callable(main_args[0]):
        return _handle_list(main_args[0])
    else:
        return _handle_list


def _get_func_call_str(func, arg, args, kwargs):
    '''Gete function call as string to print.'''
    return '{}({}{})'.format(func.__name__, arg, '...' if len(args) > 1 or kwargs else '')


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



@handle_list(print_func_call=True, return_result=False)
def print_square_2(num):
    '''Same as square(), but prints instead of returning. Tests print_func_call and return_result.

    >>> print_square_2(3)
        9
    >>> print_square_2([4, 5, 6])
    Calling print_square_2(4...):
        16
    Calling print_square_2(5...):
        25
    Calling print_square_2(6...):
        36
    '''
    print('\t{}'.format(square(num)))
