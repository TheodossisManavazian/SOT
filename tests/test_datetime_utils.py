import datetime
from unittest import TestCase
from sot_service.utils.datetime_utils import epoch_to_date, days_between_dates


class TestDatetimeUtils(TestCase):
    def test__epoch_to_date(self):
        self.assertEqual(epoch_to_date(1670489157000), datetime.date(2022, 12, 8))
        self.assertEqual(epoch_to_date("1670489157000"), datetime.date(2022, 12, 8))
        self.assertEqual(epoch_to_date("1"), datetime.date(1969, 12, 31))
        with self.assertRaises(ValueError):
            epoch_to_date("________")
