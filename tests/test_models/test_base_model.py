#!/usr/bin/python3

import unittest
from datetime import datetime
from models.base_model import BaseModel

class TestBaseModel(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
