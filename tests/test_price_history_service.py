import datetime
from unittest import TestCase, mock
from unittest.mock import MagicMock

import pandas as pd

from sot_service.services import price_history_service as under_test

# TODO: Tests are broken, function works
class TestPriceHistoryService(TestCase):

    @mock.patch("SOT_refactor.sot_service.services.price_history_service.datetime")
    @mock.patch("SOT_refactor.sot_service.services.price_history_service.get_price_history_dataframe")
    def test__is_updated_today__updated_today__returns_True(self, phdf, date_mock):
        date_mock.datetime.today.return_value = datetime.datetime(2022, 10, 10, 10, 10, 10)
        phdf.return_value = self.mock_price_history_df(datetime.datetime(2022, 10, 10, 8, 39, 0))
        self.assertTrue(under_test.is_updated_today(MagicMock(), "blah"))

    @mock.patch("SOT_refactor.sot_service.services.price_history_service.datetime")
    @mock.patch("SOT_refactor.sot_service.services.price_history_service.get_price_history_dataframe")
    def test__is_updated_today__updated_yesterday__returns_False(self, phdf, date_mock):
        date_mock.datetime.today.return_value = datetime.datetime(2022, 10, 11, 10, 10, 10)
        phdf.return_value = self.mock_price_history_df(datetime.datetime(2022, 10, 10, 8, 39, 0))
        self.assertFalse(under_test.is_updated_today(MagicMock(), "blah"))

    @mock.patch("SOT_refactor.sot_service.services.price_history_service.datetime")
    @mock.patch("SOT_refactor.sot_service.services.price_history_service.get_price_history_dataframe")
    def test__is_updated_today__updated_yesterday__before_market_open__returns_True(self, phdf, date_mock):
        date_mock.datetime.today.return_value = datetime.datetime(2022, 10, 11, 1, 10, 10)
        phdf.return_value = self.mock_price_history_df(datetime.datetime(2022, 10, 10, 8, 39, 0))
        self.assertTrue(under_test.is_updated_today(MagicMock(), "blah"))

    @mock.patch("SOT_refactor.sot_service.services.price_history_service.datetime")
    @mock.patch("SOT_refactor.sot_service.services.price_history_service.get_price_history_dataframe")
    def test__is_updated_today__updated_today__during_market_hours__returns_True(self, phdf, date_mock):
        date_mock.datetime.today.return_value = datetime.datetime(2022, 10, 10, 17, 10, 10)
        phdf.return_value = self.mock_price_history_df(datetime.datetime(2022, 10, 10, 14, 55, 0))
        self.assertTrue(under_test.is_updated_today(MagicMock(), "blah"))


    @staticmethod
    def mock_price_history_df(date: datetime.datetime) -> pd.DataFrame:
        raw_df = {
            'open': 100,
            'high': 100,
            'low': 100,
            'close': 100,
            'volume': 100,
            'datetime': date
        }
        df = pd.DataFrame([raw_df])
        df['datetime'] = pd.to_datetime(df['datetime'])
        df.index = df.pop("datetime")
        return df