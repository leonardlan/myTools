'''JSON related util functions.'''

import collections
import json
import logging
import os
import tempfile


TEMP_DATA_JSON_FILE = os.path.join(tempfile.gettempdir(), 'python_interactive_data_dump.json')


def dump_json(data, file_path=TEMP_DATA_JSON_FILE, indent=4, sort_keys=True, **dump_kwargs):
    '''Dump data to JSON file.'''
    with open(file_path, 'w') as fil:
        json.dump(data, fil, indent=indent, sort_keys=sort_keys, **dump_kwargs)
    logging.info('Data written to %s' % file_path)


def load_json(file_path=TEMP_DATA_JSON_FILE, as_string=False):
    '''Load data from JSON file.'''
    with open(file_path, 'r') as fil:
        data = json.load(fil)
    return _convert(data) if as_string else data


def _convert(data):
    '''Convert unicode to string in dict.

    https://stackoverflow.com/questions/1254454/fastest-way-to-convert-a-dicts-keys-values-from-unicode-to-str
    '''
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(_convert, data.items()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(_convert, data))
    return data
