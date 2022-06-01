from .constants import IPFS_URL, SERVER_URL, PUB_KEY_STRING, PUBLIC_KEY, PRIVATE_KEY, DATA, SIGNATURE
from client.functions import init_user, add_password, get_passwords, edit_password
import requests
import unittest


init_user(PUB_KEY_STRING, SIGNATURE, DATA)


class EditPasswordsTest(unittest.TestCase):
    """Tests for passwords edition."""

    def test_address_change(self):
        """Check change of address in IPFS."""

        address_before = add_password(PUBLIC_KEY, PUB_KEY_STRING, SIGNATURE, DATA, "test.service", "test.login", "test.password_before").strip('"')
        address_after = edit_password(PUBLIC_KEY, PUB_KEY_STRING, SIGNATURE, DATA, address_before, "test.service", "test.login", "test.password_after").strip('"')
        
        self.assertNotEqual(address_before, address_after)

    def test_password_change(self):
        """Check that password is actually different."""

        address_before = add_password(PUBLIC_KEY, PUB_KEY_STRING, SIGNATURE, DATA, "test.service", "test.login", "test.password_before").strip('"')
        password_before = requests.get("https://ipfs.infura.io/ipfs/{}".format(address_before)).json()["password"]

        address_after = edit_password(PUBLIC_KEY, PUB_KEY_STRING, SIGNATURE, DATA, address_before, "test.service", "test.login", "test.password_after").strip('"')
        password_after = requests.get("https://ipfs.infura.io/ipfs/{}".format(address_after)).json()["password"]

        self.assertNotEqual(password_before, password_after)

