from api_tests.init_user_test import InitUserTests
from api_tests.add_password_test import AddPasswordTests
from api_tests.get_passwords_test import GetPasswordsTest
from api_tests.edit_password_test import EditPasswordsTest
from api_tests.delete_password_test import DeletePasswordsTest
import unittest


tests = unittest.TestSuite()

tests.addTest(unittest.makeSuite(InitUserTests))
tests.addTest(unittest.makeSuite(AddPasswordTests))
tests.addTest(unittest.makeSuite(GetPasswordsTest))
tests.addTest(unittest.makeSuite(EditPasswordsTest))
tests.addTest(unittest.makeSuite(DeletePasswordsTest))

unittest.TextTestRunner().run(tests)

