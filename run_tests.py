from api_tests.add_password_test import AddPasswordTests
from api_tests.get_passwords_test import GetPasswordsTest
import unittest


tests = unittest.TestSuite()
tests.addTest(unittest.makeSuite(AddPasswordTests))
tests.addTest(unittest.makeSuite(GetPasswordsTest))
unittest.TextTestRunner().run(tests)
