'''Functions used in Python CLI.'''
from lancore import INFO, _is_text, _var_name, human_int


def find(haystack, needle, all=False, first=False, ignore_case=True, max_results=50):
    '''Recursively finds path to needle in haystack (can be list or dict).

    Example:
        >>> haystack = {
            'fruits': [
                {'color': 'yellow', 'name': 'banana'},
                {'color': 'red', 'name': 'strawberry'},
                {'color': 'yellow', 'name': 'lemon'}],
            'vegetables': [
                {'color': 'green', 'name': 'green pepper'}
        ]}

        >>> find(haystack, 'pepper')
        INFO: Searching...
        haystack['vegetables'][0]['name']: green pepper
        INFO: Found 1 result

        >>> haystack['vegetables'][0]['name']
        'green pepper'

        >>> find(haystack, 'cucumber')
        INFO: Searching...
        INFO: Not found

        >>> find(haystack, 'yellow')
        INFO: Searching...
        haystack['fruits'][0]['color']: yellow
        haystack['fruits'][2]['color']: yellow
        INFO: Found 2 results

    Args:
        haystack (dict or list): A dict or list.
        needle (anything): Target to find.
        all (bool): Shows all results if True. Up to max_results otherwise.
        first (bool): Returns first result if True. All results otherwise.
        ignore_case (bool): Case-insensitive if True.
        max_results (int): Max number of results to return. Unlimited if negative or zero.

    Returns:
        (list of paths to needle): Results as list of keys to needle.
    '''
    INFO('Searching...')
    all_ = all
    results = _find(haystack, needle, first, ignore_case)
    if not results:
        INFO('Not found')
        return
    for index, result in enumerate(results):
        if not all_ and index >= max_results > 0:
            # Max number of results reached.
            print 'Displayed first %i results...' % max_results
            break

        # Print path to value and value itself.
        path = ''
        for attr in result:
            if _is_text(attr):
                path += "['%s']" % attr
            else:
                path += '[%s]' % attr
        print '%s%s:' % (_var_name(haystack), path),
        print eval('haystack%s' % path)
    num_results = len(results)
    if not first:
        INFO('Found %s result%s' % (human_int(num_results), 's' if num_results > 1 else ''))


def _find(haystack, needle, first, ignore_case):
    '''Recursive helper for find().'''
    results = []
    if isinstance(haystack, dict):
        iterable = sorted(haystack.iteritems())
    elif isinstance(haystack, list):
        iterable = enumerate(haystack)
    else:
        # Not sure how to iterate or if iterable.
        return results

    for key, val in iterable:
        if isinstance(val, (dict, list)):
            recursive_results = _find(val, needle, first, ignore_case)
            if recursive_results:
                results.extend([[key] + res for res in recursive_results])
                if first:
                    break
        elif val == needle:
            results.append([key])
            if first:
                break
        elif val:
            if _is_text(val) and _is_text(needle):
                if ignore_case:
                    if needle.lower() in val.lower():
                        # Is text and in val, case-insensitive.
                        results.append([key])
                        if first:
                            break
                else:
                    if needle in val:
                        # Is text and in val, case-sensitive.
                        results.append([key])
                        if first:
                            break

    return results
