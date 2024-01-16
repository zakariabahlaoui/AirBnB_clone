#!/usr/bin/python3
"""Unittests for models/city.py"""

import unittest
from models.city import City


class TestCity(unittest.TestCase):
    """Contains test cases for the City class"""

    def test_init(self):
        """Test instantiation"""

        obj = City()
        self.assertIsInstance(obj, City)

        attributes = {"state_id": str, "name": str}
        for att_name, att_type in attributes.items():
            self.assertTrue(hasattr(obj, att_name))
            self.assertEqual(type(getattr(obj, att_name, None)), att_type)


if __name__ == "__main__":
    unittest.main()
