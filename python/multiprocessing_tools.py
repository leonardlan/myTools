'''Multiprocessing tools.'''

import multiprocessing


def run_func(func, args, processes=None, ordered=False, print_result=True):
    '''Creates multiprocessing pool and run function call on single arguments.

    Uses imap() to allow printing progress after each call, instead of having to wait for all calls
    to finish.

    Args:
        func (func(arg)): Function to call that takes a single argument.
            Returns a tuple of two. First one is the result. Second one is a string to print after
            function call. Makes it easier to see progress.
        args ([arg]): List of single arguments to pass to func.
        processes (int or None): Number of CPUs to use. Uses system CPUs if None.
        ordered (bool): Uses imap() if True. imap_unordered() otherwise.

    Returns:
        list: List of results from function call. None if failed.
    '''
    processes = multiprocessing.cpu_count() if processes is None else processes

    # Launch multiprocessing pool.
    pool = multiprocessing.Pool(processes=processes)
    results = []
    count = len(args)
    imap_func = pool.imap if ordered else pool.imap_unordered
    try:
        for ind, result in enumerate(imap_func(func, args)):
            # Print progress.
            print '{}/{}: {}'.format(ind + 1, count, result if print_result else '')

            results.append(result)
    except Exception as err:
        print 'One of the function calls errored: {}'.format(err)

    return results
