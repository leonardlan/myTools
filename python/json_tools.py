'''JSON related functions for loading from and dumping to .json files.'''


import collections
import json
import logging
import os
import tempfile

import python_compatibility


TEMP_DATA_JSON_FILE = os.path.join(tempfile.gettempdir(), 'python_interactive_data_dump.json')


def dump_json(data, file_path=TEMP_DATA_JSON_FILE, indent=4, sort_keys=True, **dump_kwargs):
    '''Dump data to JSON file.

    Args:
        data (dict or list): Dict or list with serializable data to dump into a .json file.

    Kwargs:
        file_path (str): File path to write JSON file. Defaults to TEMP_DATA_JSON_FILE.
        indent (int): Number of spaces to indent in JSON file.
        sort_keys (bool): If True, output of dictionaries will be sorted by key.
        dump_kwargs (dict): Kwargs to pass to json.dump().
    '''
    with open(file_path, 'w') as fil:
        json.dump(data, fil, indent=indent, sort_keys=sort_keys, **dump_kwargs)
    logging.info('Data written to {}'.format(file_path))


def load_json(file_path=TEMP_DATA_JSON_FILE, as_string=False):
    '''Load data from JSON file.

    Kwargs:
        file_path (str): File path to read JSON file. Defaults to TEMP_DATA_JSON_FILE.
        as_string (bool): If True, converts unicode to string in result.

    Returns:
        dict/list: Data from JSON file.
    '''
    with open(file_path, 'r') as fil:
        data = json.load(fil)
    return _convert(data) if as_string else data


def _convert(data):
    '''Convert unicode to string in dict.

    https://stackoverflow.com/questions/1254454/fastest-way-to-convert-a-dicts-keys-values-from-unicode-to-str
    '''
    if python_compatibility.is_string(data):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(_convert, data.items()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(_convert, data))
    return data
