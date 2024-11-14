import unittest
from datetime import datetime, timedelta
from nexler.utils import dt_util


class TestDtUtil(unittest.TestCase):

    def test_format_date(self):
        date = datetime(2023, 5, 29)
        self.assertEqual(dt_util.format_date(date), '2023-05-29')

    def test_human_date(self):
        date = datetime(2023, 5, 29)
        self.assertEqual(dt_util.human_date(date), '29/05/2023')

    def test_parse_date(self):
        date_str = '2023-05-29'
        self.assertEqual(dt_util.parse_date(date_str), datetime(2023, 5, 29))

    def test_add_days(self):
        date = datetime(2023, 5, 29)
        self.assertEqual(dt_util.add_days(date, 1), datetime(2023, 5, 30))

    def test_add_hours(self):
        date = datetime(2023, 5, 29)
        self.assertEqual(dt_util.add_hours(date, 1), datetime(2023, 5, 29, 1))

    def test_add_minutes(self):
        date = datetime(2023, 5, 29)
        self.assertEqual(dt_util.add_minutes(date, 1), datetime(2023, 5, 29, 0, 1))

    def test_add_years(self):
        date = datetime(2023, 5, 29)
        self.assertEqual(dt_util.add_years(date, 1), datetime(2024, 5, 29))

    def test_time_difference(self):
        date1 = datetime(2023, 5, 29)
        date2 = datetime(2023, 5, 30)
        self.assertEqual(dt_util.time_difference(date1, date2), timedelta(days=1))

    def test_days_difference(self):
        date1 = datetime(2023, 5, 29)
        date2 = datetime(2023, 5, 30)
        self.assertEqual(dt_util.days_difference(date1, date2), 1)

    def test_hours_difference(self):
        date1 = datetime(2023, 5, 29)
        date2 = datetime(2023, 5, 29, 1)
        self.assertEqual(dt_util.hours_difference(date1, date2), 1)

    def test_minutes_difference(self):
        date1 = datetime(2023, 5, 29)
        date2 = datetime(2023, 5, 29, 0, 1)
        self.assertEqual(dt_util.minutes_difference(date1, date2), 1)


if __name__ == '__main__':
    unittest.main()
