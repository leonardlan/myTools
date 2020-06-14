'''JSON related util functions.'''

import json
import os
import logging
import tempfile


TEMP_DATA_JSON_FILE = os.path.join(tempfile.gettempdir(), 'python_interactive_data_dump.json')


def dump_json(data, file_path=TEMP_DATA_JSON_FILE, indent=4, sort_keys=True, **dump_kwargs):
    '''Dump data to JSON file.'''
    with open(file_path, 'w') as fil:
        json.dump(data, fil, indent=indent, sort_keys=sort_keys, **dump_kwargs)
    logging.info('Data written to %s' % file_path)


def load_json(file_path=TEMP_DATA_JSON_FILE):
    '''Load data from JSON file.'''
    with open(file_path, 'r') as fil:
        return json.load(fil)
