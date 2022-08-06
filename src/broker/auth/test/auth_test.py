import pytest
import unittest
from mock import patch

from broker import auth
import broker


class TestAuth(unittest.TestCase):

    # def setUp(self) -> None:

    # def tearDown(self) -> None:
    #     auth.input = input

    def test_constructor_auto(self):

        with patch.object(auth.Auth, 'read_file') as mock_read_file:
            mock_read_file.return_value = 0

            test_obj = auth.Auth.from_file("/bin/Authfile")
            # with pytest.raises(Exception) as e_info:
            # assert test_obj.bin_path == "../bin"
            assert test_obj.auth_file == "../bin/Authfile"
            self.assertTrue(mock_read_file.called)

        with patch.object(auth.Auth, 'read_file') as mock_read_file:

            with patch.object(auth.Auth, 'input_account_data') as mock_input_account_data:
                mock_read_file.return_value = 1
                test_obj_2 = auth.Auth()
                self.assertTrue(mock_read_file.called)
                self.assertTrue(mock_input_account_data.called)

    def test_input_account_data(self):
        auth.input = lambda: '11223344'


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestAuth('test_constructor_auto'))
    suite.addTest(TestAuth('test_input_account_data'))
    return suite


if __name__ == '__main__':
    # unittest.main()
    runner = unittest.TextTestRunner()
    runner.run(suite())
