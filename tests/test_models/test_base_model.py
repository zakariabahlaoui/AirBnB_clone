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

    def test_to_dict(self):
        m_model = BaseModel()
        m_model_dict = m_model.to_dict()

        self.assertIsInstance(m_model_dict, dict)
        self.assertIn('__class__', m_model_dict)
        self.assertEqual(m_model_dict['__class__'], 'BaseModel')
        self.assertIn('id', m_model_dict)
        self.assertEqual(m_model_dict['id'], m_model.id)
        self.assertIn('created_at', m_model_dict)
        self.assertEqual(m_model_dict['created_at'], m_model.created_at.isoformat())
        self.assertIn('updated_at', m_model_dict)
        self.assertEqual(m_model_dict['updated_at'], m_model.updated_at.isoformat())

    def test_str(self):
        m_model = BaseModel()
        m_model_str = str(m_model)

        self.assertIsInstance(m_model_str, str)
        self.assertIn('BaseModel', m_model_str)
        self.assertIn(m_model.id, m_model_str)
        self.assertIn(str(m_model.__dict__), m_model_str)

if __name__ == '__main__':
    unittest.main()
