#!/usr/bin/python3
"""Defines unittests for models/base_model.py.
Unittest classes:
    TestBaseModel_save
    TestBaseModel_to_dict
"""

import unittest
from datetime import datetime
from models.base_model import BaseModel

class TestBaseModel(unittest.TestCase):
    """Unittests for testing init, save, and test_str methods of the BaseModel class."""


    def test_init(self):
        m_model = BaseModel()
        self.assertIsInstance(m_model.id, str)
        self.assertIsInstance(m_model.created_at, datetime)
        self.assertIsInstance(m_model.updated_at, datetime)

    def test_save(self):
        m_model = BaseModel()
        ini_updated_at = m_model.updated_at
        curr_at = m_model.save()
        self.assertNotEqual(ini_updated_at, curr_at)

    def test_str(self):
        m_model = BaseModel()
        m_str = str(m_model)

        self.assertIsInstance(m_str, str)
        self.assertIn('BaseModel', m_str)
        self.assertIn(m_model.id, m_str)
        self.assertIn(str(m_model.__dict__), m_str)

if __name__ == '__main__':
    unittest.main()
