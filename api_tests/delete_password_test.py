from .constants import IPFS_URL, SERVER_URL, PUB_KEY_STRING, PUBLIC_KEY, PRIVATE_KEY, DATA, SIGNATURE
from client.functions import init_user, add_password, get_passwords, delete_password
import requests
import unittest


# Create new user
init_user(PUB_KEY_STRING, SIGNATURE, DATA)


class DeletePasswordsTest(unittest.TestCase):
    def test_passwords_count(self):
        address = add_password(PUBLIC_KEY, PUB_KEY_STRING, SIGNATURE, DATA, "test.service", "test.login", "test.password").strip('"')
        passwords_count_before = len(get_passwords(PUB_KEY_STRING, PRIVATE_KEY, SIGNATURE, DATA))
        delete_password(PUBLIC_KEY, PUB_KEY_STRING, SIGNATURE, DATA, address)
        passwords_count_after = len(get_passwords(PUB_KEY_STRING, PRIVATE_KEY, SIGNATURE, DATA))

        self.assertNotEqual(passwords_count_before, passwords_count_after)

