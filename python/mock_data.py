'''Global mock data variables for use in testing/Python CLI.'''
import os

from json_tools import load_json
from lancore import MYTOOLS


# Example data to fiddle around with.
PEOPLE = load_json(os.path.join(MYTOOLS, 'mock_data', 'people.json'))
PEOPLE_DICT = {people['id']: people for people in PEOPLE}
