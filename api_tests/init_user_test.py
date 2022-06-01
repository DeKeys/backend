from .constants import IPFS_URL, SERVER_URL, PUB_KEY_STRING, PUBLIC_KEY, PRIVATE_KEY, DATA, SIGNATURE
from client.functions import init_user, add_password, get_passwords
import requests
import unittest


class InitUserTests(unittest.TestCase):
    """Tests for user creation."""

    def test_successful_init(self):
        """Test for successfull creation of user."""

        self.assertEqual(init_user(PUB_KEY_STRING, SIGNATURE, DATA), True)
    
    def test_invalid_signature(self):
        """Test for invalid signature."""

        self.assertEqual(init_user(PUB_KEY_STRING, SIGNATURE + b"a", DATA), False) 

    def test_data_overflow(self):
        """Test for data overflow."""

        self.assertEqual(init_user(PUB_KEY_STRING, SIGNATURE, DATA + b"a"), False)

