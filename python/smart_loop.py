'''Includes smart_loop() for running a function on a list of items and printing progress report.'''

import time


PRE_FUNC_CALL_STR = '> Running {func_name}({item}) ({index}/{count} {percentage:.1f}%)...'
POST_FUNC_CALL_STR = '> {func_name}({item}) took {seconds:.1f} seconds'
ERROR_MESSAGE_STR = 'Errored while running {func_name}({item}): {error}'
REPORT_STR = 'Ran {func_name}() on {count} items in {seconds:.1f} seconds ({successful_count}/' \
    '{count} successful)'


def smart_loop(func, items, pre_func_call_str=PRE_FUNC_CALL_STR, print_pre_func_call_str=True,
        post_func_call_str=POST_FUNC_CALL_STR, print_post_func_call_str=True,
        error_message_str=ERROR_MESSAGE_STR, print_error_message_str=True,
        report_str=REPORT_STR, print_report_str=True,
        exception=Exception, raise_exception=True, **kwargs):
    '''Run function on each given item. Prints progress along the way, tracks error messages, and
    return results.

    Args:
        func (func): Function to run each item on.
        items (list): List of items to call function through.

        pre_func_call_str (str): Progress line to print before every item call. Has string
            formatting for func_name (str), item (str), index (int), count (int), and percentage
            (float).
        print_pre_func_call_str (bool): Print pre_func_call_str if True.

        post_func_call_str (str): Progress line to print after every item call. Has string
            formatting for func_name (str), item (str), and seconds (float).
        print_post_func_call_str (bool): Print post_func_call_str if True.

        error_message_str (str): Error message to print when exception thrown from function call.
            Has string formatting for func_name (str), item (str), and error (exception).
        print_error_message_str (bool): Print error_message_str if True.

        report_str (str): String to print after iterating items. Has string formatting for:
            func_name (str): Function name.
            count (int): Total number of items.
            seconds (float): Seconds the loop of calls took.
            successful_count (int): Number of calls without error raised.
        print_report_str (bool): Print print_report_str if True.

        exception (Exception): Exception to catch from function call (ie. ValueError). Note that
            BaseException catches all exceptions, including GeneratorExit, KeyboardInterrupt, and
            SystemExit. Just "Exception" won't. Use BaseException with caution.
        raise_exception (bool): If True, raise Exception from function call. False will continue
            iterating rest of the items.

        kwargs (dict): Kwargs passed to function call.

    Returns:
        [dict]: List of function call results as dict. If successful:
            {'successful': True, 'result': <result from function call>}
        If exception raised:
            {'successful': False, 'message': <message (string)>, 'error': <error raised>}.
    '''
    results = []
    count = len(items)
    format_kwargs = {'func_name': func.__name__}
    start = time.time()
    successful_count = 0
    for index, item in enumerate(items):
        format_kwargs['item'] = str(item)

        # Print progress before function call.
        if print_pre_func_call_str:
            percentage = float(index + 1) / count
            print(
                pre_func_call_str.format(
                    index=index + 1, count=count, percentage=percentage * 100, **format_kwargs))

        # Start timer for function call on this item.
        item_start = time.time()

        # Call function.
        try:
            res = func(item, **kwargs)
        except exception as error:
            message = error_message_str.format(error=error, **format_kwargs)

            # Raise exception if specified.
            if raise_exception:
                raise exception(message)

            if print_error_message_str:
                print(message)
            results.append({'successful': False, 'message': message, 'error': error})
        else:
            results.append({'successful': True, 'result': res})
            successful_count += 1

        # Print progress after function call.
        if print_post_func_call_str:
            print(post_func_call_str.format(seconds=time.time() - item_start, **format_kwargs))

    if print_report_str:
        print(
            report_str.format(
                func_name=func.__name__, count=count, seconds=time.time() - start,
                successful_count=successful_count))

    return results
