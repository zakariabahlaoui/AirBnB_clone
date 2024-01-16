#!/usr/bin/python3
"""Unittests for models/amenity.py"""

import unittest
from models.amenity import Amenity


class TestAmenity(unittest.TestCase):
    """Contains test cases for the Amenity class"""

    def test_init(self):
        """Test instantiation"""

        obj = Amenity()
        self.assertIsInstance(obj, Amenity)

        attributes = {"name": str}
        for att_name, att_type in attributes.items():
            self.assertTrue(hasattr(obj, att_name))
            self.assertEqual(type(getattr(obj, att_name, None)), att_type)


if __name__ == "__main__":
    unittest.main()
