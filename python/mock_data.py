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
