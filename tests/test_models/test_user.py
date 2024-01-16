#!/usr/bin/python3
"""Unittests for models/user.py"""

import unittest
from models.user import User


class TestUser(unittest.TestCase):
    """Contains test cases for the User class"""

    def test_init(self):
        """Test instantiation"""

        obj = User()
        self.assertIsInstance(obj, User)

        attributes = {
            "email": str,
            "password": str,
            "first_name": str,
            "last_name": str,
        }
        for att_name, att_type in attributes.items():
            self.assertTrue(hasattr(obj, att_name))
            self.assertEqual(type(getattr(obj, att_name, None)), att_type)


if __name__ == "__main__":
    unittest.main()
