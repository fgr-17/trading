import pytest
import unittest
from mock import patch

import pyhomebroker as phb

from broker import Broker


class TestHbAuth(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_input_account_data(self):
        self.assertEqual(0, 0)


class TestBroker(unittest.TestCase):

    def test_constructor_ok(self):
        b = Broker(265)
        assert b is not None

    def test_start_session(self):
        # with patch.object(phb., 'read_file') as mock_read_file:
        assert True

    def test_end_session(self):
        assert True

    def test_ticker_get_data(self):
        assert True

    def test_get_dataset(self):
        assert True

    def test_ticker_get_current_price(self):
        assert True

    def test_portfolio_get_current_positions(self):
        assert True

    def test_changes2orders(self):
        assert True

    def test_execute_orders(self):
        assert True

    def test_sell_order(self):
        assert True

    def test_buy_order(self):
        assert True


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestHbAuth('test_input_account_data'))
    return suite


if __name__ == '__main__':
    # unittest.main()
    runner = unittest.TextTestRunner()
    runner.run(suite())
