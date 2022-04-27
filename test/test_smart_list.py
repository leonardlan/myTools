import unittest

from collections import Counter

from smart_list import SmartList


class Dog(object):

    too_old = 10

    def __init__(self, name, breed, color=None, age=None, ig_handle=None):
        self.name = name
        self.breed = breed
        self.color = color
        self.age = age
        self.ig_handle = ig_handle

    def __repr__(self):
        return 'Dog({}, {}, {})'.format(self.name, self.breed, self.color)

    @property
    def is_old(self):
        return self.age is not None and self.age >= self.too_old

    def bark(self):
        print('Woof!')


# Setup DOGS.
LULU = Dog('Lulu', 'Maltese', color='white')
QI_WAN = Dog('QiWan', 'Bichon Frise', color='white')
SNOWY = Dog('Snowy', 'Wire Fox Terrier', color='white')
SCOOBY = Dog('Scooby Doo', 'Great Dane', color='brown', age=10)
FLUFFY = Dog('Fluffy', 'Samoyed', color='white', age=5)
SNOOPY = Dog('Snoopy', 'Spotted White Beagle', color='white')
MAYA = Dog('Maya', 'Samoyed', color='white', ig_handle='mayapolarbear')

DOGS = SmartList(
    LULU,
    QI_WAN,
    SNOWY,
    SCOOBY,
    FLUFFY,
    SNOOPY,
    MAYA,
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

    def test_dogs_basic(self):
        self.assertEqual(str(DOGS), 'SmartList(7 Dog)')
        self.assertEqual(DOGS.types, [Dog])
        self.assertEqual(DOGS.all_same_type, True)
        self.assertEqual(DOGS.keys, [])

    def test_dogs_filter(self):
        self.assertEqual(DOGS.filter(is_old=True), SmartList(SCOOBY))
        self.assertEqual(
            DOGS.filter(color='white'), SmartList(LULU, QI_WAN, SNOWY, FLUFFY, SNOOPY, MAYA))
        self.assertEqual(DOGS.filter(breed='Samoyed'), SmartList(FLUFFY, MAYA))

    def test_dogs_attrs(self):
        self.assertEqual(DOGS.attr('name'),
            ['Lulu', 'QiWan', 'Snowy', 'Scooby Doo', 'Fluffy', 'Snoopy', 'Maya'])
        self.assertEqual(DOGS.attr('age', ignored_values=[None]), [10, 5])
        self.assertEqual(DOGS.min('age'), 5)
        self.assertEqual(DOGS.max('age'), 10)
        self.assertEqual(DOGS.average('age'), 7.5)
        self.assertEqual(
            DOGS.attr_counter('breed'),
            Counter({'Samoyed': 2, 'Wire Fox Terrier': 1, 'Bichon Frise': 1, 'Great Dane': 1, 'Maltese': 1, 'Spotted White Beagle': 1}))

        self.assertEqual(DOGS.attr_counter('color'), Counter({'white': 6, 'brown': 1}))

        self.assertEqual(
            DOGS.attrs(['name', 'breed']),
            [
                ['Lulu', 'Maltese'],
                ['QiWan', 'Bichon Frise'],
                ['Snowy', 'Wire Fox Terrier'],
                ['Scooby Doo', 'Great Dane'],
                ['Fluffy', 'Samoyed'],
                ['Snoopy', 'Spotted White Beagle'],
                ['Maya', 'Samoyed']]
            )


if __name__ == '__main__':
    unittest.main()
