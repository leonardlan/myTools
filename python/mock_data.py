'''Global mock data variables for use in testing/Python CLI.'''
import os

from json_tools import load_json
from my_settings import MYTOOLS


MOCK_DATA = os.path.join(MYTOOLS, 'test', 'mock_data')

# Example data to fiddle around with.
DOGS = load_json(os.path.join(MOCK_DATA, 'dogs.json'))
DOGS_DICT = {dog['id']: dog for dog in DOGS}
PEOPLE = load_json(os.path.join(MOCK_DATA, 'people.json'))
PEOPLE_DICT = {person['id']: person for person in PEOPLE}


class SomeObject(object):
    pass

    @property
    def some_property(self):
        return 'Some property'


TYPE_TO_VAL = {
    'string': 'Hello!',
    'int': 1234,
    'float': 3.14,
    'list': ['Vancouver', 'Calgary', 'Montreal'],
    'tuple': (0, 1, 1, 2, 3, 5, 8, 13, 21, 34),
    'set': set([1, 2, 3, 4]),
    'dict': {
        'British Columbia': {'capital': 'Victoria'},
        'Ontario': {'capital': 'Toronto'}
    },
    'some_object': SomeObject(),
    'class': SomeObject
}
