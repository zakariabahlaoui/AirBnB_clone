#!/usr/bin/python3
"""Unittests for models/place.py"""

import unittest
from models.place import Place


class TestPlace(unittest.TestCase):
    """Contains test cases for the City class"""

    def test_init(self):
        """Test instantiation"""

        obj = Place()
        self.assertIsInstance(obj, Place)

        attributes = {
            "city_id": str,
            "user_id": str,
            "name": str,
            "description": str,
            "number_rooms": int,
            "number_bathrooms": int,
            "max_guest": int,
            "price_by_night": int,
            "latitude": float,
            "longitude": float,
            "amenity_ids": list,
        }
        for att_name, att_type in attributes.items():
            self.assertTrue(hasattr(obj, att_name))
            self.assertEqual(type(getattr(obj, att_name, None)), att_type)


if __name__ == "__main__":
    unittest.main()
