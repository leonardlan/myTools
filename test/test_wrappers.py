import unittest

from wrappers import square


class TestHandleList(unittest.TestCase):

    def test_square(self):
        self.assertEqual(square(5), 25)
        self.assertEqual(square([1, 2, 3, 4, 6]), [1, 4, 9, 16, 36])
        self.assertRaises(RuntimeError, square, [6, 7, 'asdf'])


if __name__ == '__main__':
    unittest.main()
