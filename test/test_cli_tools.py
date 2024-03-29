import unittest

from cli_tools import _find, get


EXAMPLE_DATA = {
    'fruits': [
        {'color': 'yellow', 'name': 'banana'},
        {'color': 'red', 'name': 'strawberry'},
        {'color': 'yellow', 'name': 'lemon'}
    ],
    'vegetables': [
        {'color': 'green', 'name': 'green pepper'}
    ],
    'contacts': {
        'John Smith': {
            'gender': 'male',
            'email': 'john.smith@gmail.com'
        },
        'Jane Smithers': {
            'gender': 'female',
            'email': 'jane.smithers@gmail.com'
        }
    },
    'comment': 'Some comment',
    'countries_tuple': ('Afghanistan', 'Albania', 'USA', 'Canada'),
    'top_capitals_set':
        set(['London', 'Tokyo', 'Paris', 'Rome', 'Washington D.C.', 'Berlin', 'Buenos Aires',
                    'Bangkok'])
}


class TestFind(unittest.TestCase):

    def test_find_key(self):
        self.assertEqual(_find(EXAMPLE_DATA, 'fruits', False, True), [['fruits']])
        self.assertEqual(
            _find(EXAMPLE_DATA,'smith', False, True),
            [
                ['contacts', 'Jane Smithers'],
                ['contacts', 'John Smith'],
            ])
        self.assertEqual(
            _find(EXAMPLE_DATA, 'jane', False, True),
            [
                ['contacts', 'Jane Smithers']])

    def test_find_val(self):
        self.assertEqual(_find(EXAMPLE_DATA, 'lemon', False, True), [['fruits', 2, 'name']])
        self.assertEqual(_find(EXAMPLE_DATA, 'pepper', False, True), [['vegetables', 0, 'name']])
        self.assertEqual(_find(EXAMPLE_DATA, 'USA', False, True), [['countries_tuple', 2]])
        self.assertEqual(_find(EXAMPLE_DATA, 'Berlin', False, True), [['top_capitals_set']])

    def test_find_target_both_in_key_and_val(self):
        self.assertEqual(_find(EXAMPLE_DATA, 'comment', False, True), [['comment']])

    def test_find_multiple_results(self):
        self.assertEqual(
            _find(EXAMPLE_DATA, 'yellow', False, True),
            [['fruits', 0, 'color'], ['fruits', 2, 'color']])

    def test_case_sensitive(self):
        self.assertEqual(_find(EXAMPLE_DATA, 'Strawberry', False, False), [])
        self.assertEqual(_find(EXAMPLE_DATA, 'strawberry', False, False), [['fruits', 1, 'name']])

    def test_first(self):
        self.assertEqual(
            _find(EXAMPLE_DATA, 'smith', True, True), [['contacts', 'Jane Smithers']])


class TestGet(unittest.TestCase):

    def test_get_simple(self):
        self.assertEqual(get(EXAMPLE_DATA, 'contacts', 'John Smith', 'gender'), 'male')

    def test_get_in_list_and_dict(self):
        self.assertEqual(get(EXAMPLE_DATA, 'fruits', 0, 'color'), 'yellow')

    def test_get_in_list_dict_tuple(self):
        self.assertEqual(get(EXAMPLE_DATA, 'countries_tuple', 3), 'Canada')

    def test_get_string_with_char_delimiter(self):
        self.assertEqual(get(EXAMPLE_DATA, 'fruits,0,color', delimiter=','), 'yellow')
        self.assertEqual(get(EXAMPLE_DATA, 'vegetables 0 name'), 'green pepper')
        self.assertEqual(get(EXAMPLE_DATA, 'contacts|John Smith|gender', delimiter='|'), 'male')
        self.assertEqual(
            get(EXAMPLE_DATA, 'contacts|Jane Smithers|gender', delimiter='|'), 'female')

    def test_get_non_existent(self):
        self.assertEqual(get(EXAMPLE_DATA, 'narnia'), None)

    def test_no_key(self):
        self.assertEqual(get(EXAMPLE_DATA), EXAMPLE_DATA)


if __name__ == '__main__':
    unittest.main()
