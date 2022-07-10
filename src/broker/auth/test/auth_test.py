import pytest
import unittest

from broker import auth

class TestAuth(unittest.TestCase):

    # def setUp(self) -> None:
    # def tearDown(self) -> None:

    def test_constructor(self):
        with pytest.raises(Exception) as e_info:
            test_obj = auth.Auth()
        # assert test_obj.bin_path == "../bin"
        # assert test_obj.auth_file == "../bin/Authfile"


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestAuth('test_constructor'))
    return suite


if __name__ == '__main__':
    # unittest.main()
    runner = unittest.TextTestRunner()
    runner.run(suite())
