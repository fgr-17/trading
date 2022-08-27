import pytest
import unittest
from mock import patch

from broker.auth import Auth
from broker import Broker


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

    def test_get(self):
        cut = Auth(11, 22, 33, 44)
        assert cut.get() == {'id_num': 11, 'usr': 22, 'pwd': 33, 'acc': 44}

    def test_get_id_num(self):
        cut = Auth(11, 22, 33, 44)
        assert cut.get_id_num() is 11

    def test_get_usr(self):
        cut = Auth(11, 22, 33, 44)
        assert cut.get_usr() is 22

    def test_get_pwd(self):
        cut = Auth(11, 22, 33, 44)
        assert cut.get_pwd() is 33

    def test_get_acc(self):
        cut = Auth(11, 22, 33, 44)
        assert cut.get_acc() is 44

    def test_save_file(self):
        # todo
        assert True

    def test_read_file(self):
        # todo
        assert True


def suite():
    suite = unittest.TestSuite()
    return suite


if __name__ == '__main__':
    # unittest.main()
    runner = unittest.TextTestRunner()
    runner.run(suite())
