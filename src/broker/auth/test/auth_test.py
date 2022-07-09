import unittest


class TestAuth(unittest.TestCase):

    # def setUp(self) -> None:
    # def tearDown(self) -> None:

    def test_input_account_data(self):
        self.assertEqual(0, 0)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestAuth('test_input_account_data'))
    return suite


if __name__ == '__main__':
    # unittest.main()
    runner = unittest.TextTestRunner()
    runner.run(suite())
