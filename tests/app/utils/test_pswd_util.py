import unittest
from nexler.utils import pswd_util


class TestPswdUtil(unittest.TestCase):
    def setUp(self):
        self.password = "securepassword123"
        self.password_hash = pswd_util.hash_password(self.password)

    def test_hash_password(self):
        # Ensure the hash is not equal to the original password
        self.assertNotEqual(self.password_hash, self.password)

        # Check that the hashed password is not None
        self.assertIsNotNone(self.password_hash)

        # Check that the hashed password starts with $argon2id$, the prefix for Argon2
        self.assertTrue(self.password_hash.startswith('$argon2id$'))

    def test_check_password(self):
        # Check that the original password is verified against the hash
        self.assertTrue(pswd_util.check_password(self.password, self.password_hash))
        # Check that an incorrect password is not verified
        self.assertFalse(pswd_util.check_password("wrongpassword", self.password_hash))


if __name__ == '__main__':
    unittest.main()
