#!/usr/bin/python3
"""Unittests for models/review.py"""

import unittest
from models.review import Review


class TestReview(unittest.TestCase):
    """Contains test cases for the Review class"""

    def test_init(self):
        """Test instantiation"""

        obj = Review()
        self.assertIsInstance(obj, Review)

        attributes = {"place_id": str, "user_id": str, "text": str}
        for att_name, att_type in attributes.items():
            self.assertTrue(hasattr(obj, att_name))
            self.assertEqual(type(getattr(obj, att_name, None)), att_type)


if __name__ == "__main__":
    unittest.main()
