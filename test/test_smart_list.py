import unittest

from collections import Counter
from datetime import date

from smart_list import SmartList


class Dog(object):

    too_old = 10

    def __init__(self, name, breed, color=None, ig_handle=None, birthday=None):
        self.name = name
        self.breed = breed
        self.color = color
        self.ig_handle = ig_handle
        self.birthday = birthday

    def __repr__(self):
        return 'Dog({}, {}, {})'.format(self.name, self.breed, self.color)

    @property
    def age(self):
        '''Age in years as int. None if no age.'''
        if self.birthday is None:
            return None
        today = date.today()
        return today.year - self.birthday.year - (
            (today.month, today.day) < (self.birthday.month, self.birthday.day))

    @property
    def birth_year(self):
        '''Year of birth as int. None if not specified.'''
        return self.birthday.year if self.birthday else None

    def bark(self):
        print('Woof!')


# Setup DOGS.
LULU = Dog('Lulu', 'Maltese', color='white')
QI_WAN = Dog('QiWan', 'Bichon Frise', color='white')
SNOWY = Dog('Snowy', 'Wire Fox Terrier', color='white')
SCOOBY = Dog('Scooby Doo', 'Great Dane', color='brown')
FLUFFY = Dog('Fluffy', 'Samoyed', color='white')
SNOOPY = Dog('Snoopy', 'Spotted Beagle', color='white')
MAYA = Dog(
    'Maya', 'Samoyed', color='white', ig_handle='mayapolarbear', birthday=date(2016, 7, 20))
TUCKER = Dog(
    'Tucker Budzyn', 'Golden Retriever', ig_handle='tuckerbudzyn', birthday=date(2018, 5, 2))
RIN_TIN_TIN = Dog('Rin Tin Tin', 'Golden Shepherd', color='dark sable')

DOGS = SmartList(
    LULU,
    QI_WAN,
    SNOWY,
    SCOOBY,
    FLUFFY,
    SNOOPY,
    MAYA,
    TUCKER,
    RIN_TIN_TIN,
)


class TestFind(unittest.TestCase):

    def test_empty_list(self):
        empty = SmartList()
        self.assertEqual(empty, [])
        self.assertEqual(empty.filter(), [])
        self.assertEqual(empty.filter(asdf=''), [])

    def test_one_item(self):
        one_item = SmartList('By myself')
        self.assertEqual(len(one_item), 1)
        self.assertEqual(one_item.types, [str])
        self.assertEqual(one_item.all_same_type, True)
        self.assertEqual(one_item.keys, [])
        self.assertRaises(ValueError, one_item.filter, asdf='')

    def test_dogs_basic(self):
        self.assertEqual(str(DOGS), 'SmartList(9 Dog)')
        self.assertEqual(len(DOGS), 9)
        self.assertEqual(DOGS.types, [Dog])
        self.assertEqual(DOGS.all_same_type, True)
        self.assertEqual(DOGS.keys, [])

    def test_dogs_filter_default(self):
        self.assertEqual(
            DOGS.filter(color='white'), SmartList(LULU, QI_WAN, SNOWY, FLUFFY, SNOOPY, MAYA))
        self.assertEqual(DOGS.filter(breed='Samoyed'), SmartList(FLUFFY, MAYA))

    def test_dogs_filter_with_operators(self):
        self.assertEqual(
            DOGS.filter(breed__in=['Maltese', 'Samoyed']), SmartList(LULU, FLUFFY, MAYA))
        self.assertEqual(DOGS.filter(color__is_not='white'), SmartList(SCOOBY, TUCKER, RIN_TIN_TIN))
        self.assertEqual(
            DOGS.filter(name__not_in=['Lulu', 'QiWan', 'Snowy', 'Scooby Doo', 'Fluffy']),
            SmartList(SNOOPY, MAYA, TUCKER, RIN_TIN_TIN))
        self.assertEqual(DOGS.filter(name__startswith='Sn'), SmartList(SNOWY, SNOOPY))
        self.assertEqual(DOGS.filter(name__endswith='y'), SmartList(SNOWY, FLUFFY, SNOOPY))
        self.assertEqual(DOGS.filter(breed__has='Golden'), SmartList(TUCKER, RIN_TIN_TIN))

    def test_dogs_attrs(self):
        self.assertEqual(DOGS.attr('name'),
            ['Lulu', 'QiWan', 'Snowy', 'Scooby Doo', 'Fluffy', 'Snoopy', 'Maya', 'Tucker Budzyn',
            'Rin Tin Tin'])
        self.assertEqual(DOGS.attr('birth_year', ignored_values=[None]), [2016, 2018])
        self.assertEqual(DOGS.min('birth_year'), 2016)
        self.assertEqual(DOGS.max('birth_year'), 2018)
        self.assertEqual(DOGS.average('birth_year'), 2017.0)
        self.assertEqual(
            DOGS.attr_counter('breed'),
            Counter({
                'Samoyed': 2, 'Wire Fox Terrier': 1, 'Bichon Frise': 1, 'Great Dane': 1,
                'Maltese': 1, 'Spotted Beagle': 1, 'Golden Retriever': 1,
                'Golden Shepherd': 1}))

        self.assertEqual(
            DOGS.attr_counter('color'), Counter({'white': 6, 'brown': 1, 'dark sable': 1, None: 1}))

        self.assertEqual(
            DOGS.attrs(['name', 'breed']),
            [
                ['Lulu', 'Maltese'],
                ['QiWan', 'Bichon Frise'],
                ['Snowy', 'Wire Fox Terrier'],
                ['Scooby Doo', 'Great Dane'],
                ['Fluffy', 'Samoyed'],
                ['Snoopy', 'Spotted Beagle'],
                ['Maya', 'Samoyed'],
                ['Tucker Budzyn', 'Golden Retriever'],
                ['Rin Tin Tin', 'Golden Shepherd'],
            ])


if __name__ == '__main__':
    unittest.main()
