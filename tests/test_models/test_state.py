#!/usr/bin/python3
"""Unittests for models/state.py"""

import unittest
from models.state import State


class TestState(unittest.TestCase):
    """Contains test cases for the State class"""

    def test_init(self):
        """Test instantiation"""

        obj = State()
        self.assertIsInstance(obj, State)

        attributes = {"name": str}
        for att_name, att_type in attributes.items():
            self.assertTrue(hasattr(obj, att_name))
            self.assertEqual(type(getattr(obj, att_name, None)), att_type)


if __name__ == "__main__":
    unittest.main()
