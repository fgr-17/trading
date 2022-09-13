import pytest
import unittest
from mock import patch


class TestStrategy(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_passing(self):
        self.assertEqual(0, 0)




def suite():
    suite = unittest.TestSuite()
    return suite


if __name__ == '__main__':
    # unittest.main()
    runner = unittest.TextTestRunner()
    runner.run(suite())
