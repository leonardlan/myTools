import unittest

from lancore import human_time


class TestHumanTime(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestHumanTime, self).__init__(*args, **kwargs)

    def test_negative_time(self):
        self.assertEqual(human_time(-0.5), '-0.5 seconds')
        self.assertEqual(human_time(-0.54), '-0.5 seconds')
        self.assertEqual(human_time(-0.55), '-0.6 seconds')
        self.assertEqual(human_time(-1), '-1 seconds')
        self.assertEqual(human_time(-1.5), '-1.5 seconds')
        self.assertEqual(human_time(-1.54), '-1.5 seconds')
        self.assertEqual(human_time(-1.55), '-1.6 seconds')
        self.assertEqual(human_time(-1000000), '-1000000 seconds')

    def test_zero_time(self):
        self.assertEqual(human_time(0), '0 seconds')
        self.assertEqual(human_time(0.0), '0 seconds')

    def test_between_0_and_1(self):
        self.assertEqual(human_time(0.001), '1 millisecond')
        self.assertEqual(human_time(0.01), '10 milliseconds')
        self.assertEqual(human_time(0.1), '100 milliseconds')
        self.assertEqual(human_time(0.123), '123 milliseconds')
        self.assertEqual(human_time(0.1234), '123 milliseconds')
        self.assertEqual(human_time(0.1235), '123 milliseconds')
        self.assertEqual(human_time(0.999), '999 milliseconds')

    def test_1(self):
        self.assertEqual(human_time(1), '1 second')
        self.assertEqual(human_time(1.0), '1 second')

    def test_less_than_minute(self):
        self.assertEqual(human_time(1.1), '1.1 seconds')
        self.assertEqual(human_time(10), '10 seconds')
        self.assertEqual(human_time(59), '59 seconds')
        self.assertEqual(human_time(59.5), '59.5 seconds')

    def test_decimals(self):
        self.assertEqual(human_time(1.234), '1.2 seconds')
        self.assertEqual(human_time(1.234, 2), '1.23 seconds')
        self.assertEqual(human_time(1.234, 3), '1.234 seconds')
        self.assertEqual(human_time(1.2345, 3), '1.234 seconds')

    # Test intervals.

    def test_minute(self):
        self.assertEqual(human_time(59), '59 seconds')
        self.assertEqual(human_time(59.9), '59.9 seconds')
        self.assertEqual(human_time(60), '1 minute')
        self.assertEqual(human_time(60.0), '1 minute')
        self.assertEqual(human_time(60.9), '1 minute')
        self.assertEqual(human_time(61), '1 minute and 1 second')
        self.assertEqual(human_time(61.1), '1 minute and 1 second')

    def test_hour(self):
        self.assertEqual(human_time(3599), '59 minutes and 59 seconds')
        self.assertEqual(human_time(3599.9), '59 minutes and 59 seconds')
        self.assertEqual(human_time(3600), '1 hour')
        self.assertEqual(human_time(3600.0), '1 hour')
        self.assertEqual(human_time(3600.9), '1 hour')
        self.assertEqual(human_time(3601), '1 hour and 1 second')
        self.assertEqual(human_time(3601.1), '1 hour and 1 second')
        self.assertEqual(human_time(3660), '1 hour and 1 minute')

    def test_day(self):
        self.assertEqual(human_time(86399), '23 hours and 59 minutes')
        self.assertEqual(human_time(86399.9), '23 hours and 59 minutes')
        self.assertEqual(human_time(86400), '1 day')
        self.assertEqual(human_time(86400.0), '1 day')
        self.assertEqual(human_time(86400.9), '1 day')
        self.assertEqual(human_time(86401), '1 day and 1 second')
        self.assertEqual(human_time(86401.1), '1 day and 1 second')
        self.assertEqual(human_time(86460), '1 day and 1 minute')

    def test_week(self):
        self.assertEqual(human_time(604800), '1 week')

    def test_month(self):
        self.assertEqual(human_time(2627424), '1 month')

    def test_year(self):
        self.assertEqual(human_time(31536000), '1 year')

    def test_century(self):
        self.assertEqual(human_time(3153600000), '1 century')

    def test_millennium(self):
        self.assertEqual(human_time(31536000000), '1 millennium')


if __name__ == '__main__':
    unittest.main()
