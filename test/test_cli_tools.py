import unittest

from cli_tools import _find


class TestFind(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestFind, self).__init__(*args, **kwargs)
        self.haystack = {
            'fruits': [
                {'color': 'yellow', 'name': 'banana'},
                {'color': 'red', 'name': 'strawberry'},
                {'color': 'yellow', 'name': 'lemon'}],
            'vegetables': [
                {'color': 'green', 'name': 'green pepper'}
        ]}

    def test_find_simple(self):
        self.assertEqual(_find(self.haystack, 'lemon', False, True), [['fruits', 2, 'name']])
        self.assertEqual(_find(self.haystack, 'pepper', False, True), [['vegetables', 0, 'name']])

    def test_find_multiple_results(self):
        self.assertEqual(
            _find(self.haystack, 'yellow', False, True),
            [['fruits', 0, 'color'], ['fruits', 2, 'color']])

    def test_case_sensitive(self):
        self.assertEqual(_find(self.haystack, 'Strawberry', False, False), [])
        self.assertEqual(_find(self.haystack, 'strawberry', False, False), [['fruits', 1, 'name']])


if __name__ == '__main__':
    unittest.main()
