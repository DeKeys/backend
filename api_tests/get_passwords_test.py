from .constants import IPFS_URL, SERVER_URL, PUB_KEY_STRING, PUBLIC_KEY, PRIVATE_KEY, DATA, SIGNATURE
from client.functions import init_user, add_password, get_passwords
import requests
import unittest


init_user(PUB_KEY_STRING, SIGNATURE, DATA)


class GetPasswordsTest(unittest.TestCase):
    def test_password_decryption(self):
        self.assertRaises(Exception, get_passwords(PUB_KEY_STRING, PRIVATE_KEY, SIGNATURE, DATA))
        
    def test_addresses(self):
        passwords = get_passwords(PUB_KEY_STRING, PRIVATE_KEY, SIGNATURE, DATA)
        for pwd in passwords:
            resp = requests.get("https://ipfs.infura.io/ipfs/{}".format(pwd["address"]))
            self.assertEqual(resp.status_code, 200)

