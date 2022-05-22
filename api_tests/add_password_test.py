from .constants import IPFS_URL, SERVER_URL, PUB_KEY_STRING, PUBLIC_KEY, PRIVATE_KEY, DATA, SIGNATURE
from client.functions import init_user, add_password, get_passwords
import requests
import unittest


init_user(PUB_KEY_STRING, SIGNATURE, DATA)


class AddPasswordTests(unittest.TestCase):
    def test_addition(self):
        address = add_password(PUBLIC_KEY, PUB_KEY_STRING, SIGNATURE, DATA, "test.service", "test.login", "test.password").strip('"')
        passwords_addresses = list(map(lambda x: x["address"], get_passwords(PUB_KEY_STRING, PRIVATE_KEY, SIGNATURE, DATA)))
        self.assertIn(address, passwords_addresses)

    def test_ipfs_addition(self):
        address = add_password(PUBLIC_KEY, PUB_KEY_STRING, SIGNATURE, DATA, "test.service", "test.login", "test.password").strip('"')
        resp = requests.get("https://ipfs.infura.io/ipfs/{}".format(address))
        self.assertEqual(resp.status_code, 200)

