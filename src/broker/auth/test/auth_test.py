import pytest
import unittest
from mock import patch

from broker.auth import Auth
import broker


class TestAuth(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_constructor_failed(self):

        with patch.object(Auth, 'read_file') as mock_read_file:
            mock_read_file.return_value = 0

            test_obj = Auth.from_file("...")
            assert test_obj is None
            # with pytest.raises(Exception) as e_info:
            # assert test_obj.bin_path == "../bin"
            # assert test_obj.auth_file == "bin/Authfile"
            # self.assertTrue(mock_read_file.called)

    def test_constructor_ok(self):
        test_obj = Auth.from_file("../bin/Authfile")
        assert test_obj is not None

    # def test_input_account_data(self):
    #     # input = lambda: '11223344'


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestAuth('test_constructor_failed'))
    suite.addTest(TestAuth('test_input_account_data'))
    return suite


if __name__ == '__main__':
    # unittest.main()
    runner = unittest.TextTestRunner()
    runner.run(suite())
