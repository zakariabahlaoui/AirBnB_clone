#!/usr/bin/python3
"""Unittests for models/base_model.py"""


import unittest
import uuid
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
import os
from datetime import datetime
import json
import time


class TestBaseModel(unittest.TestCase):
    """Contains test cases for the BaseModel class"""

    def tearDown(self):
        """Runs after each test"""
        # resets storage data
        FileStorage._FileStorage__objects_dict = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            # remove json file
            os.remove(FileStorage._FileStorage__file_path)

    def test_init(self):
        """Test BaseModel constructor"""

        obj = BaseModel()
        self.assertIsInstance(obj, BaseModel)

        attributes = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime
        }
        for att_name, att_type in attributes.items():
            self.assertTrue(hasattr(obj, att_name))
            self.assertEqual(type(getattr(obj, att_name, None)), att_type)

    def test_init_with_args(self):
        """Test BaseModel constructor with args"""

        dict = {
            "id": str(uuid.uuid4()),
            "name": "Julien",
            "school": "Holberthon",
            "rank": 10,
            "score": 99.9,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
        obj = BaseModel(**dict)
        self.assertIsInstance(obj, BaseModel)
        self.assertIsInstance(obj.id, str)
        self.assertEqual(obj.name, "Julien")
        self.assertEqual(obj.school, "Holberthon")
        self.assertEqual(obj.rank, 10)
        self.assertEqual(obj.score, 99.9)
        self.assertIsInstance(obj.created_at, datetime)
        self.assertIsInstance(obj.updated_at, datetime)

    def test_str(self):
        """Tests for __str__ method"""
        obj = BaseModel()
        m_str = str(obj)

        self.assertIsInstance(m_str, str)
        self.assertIn("BaseModel", m_str)
        self.assertIn(obj.id, m_str)
        self.assertIn(str(obj.__dict__), m_str)

    def test_to_dict(self):
        """Tests for to_dict() method"""

        obj = BaseModel()
        obj.name = "Julien"
        obj.school = "Holberthon"
        obj.rank = 10
        dict = obj.to_dict()
        self.assertEqual(dict["__class__"], type(obj).__name__)
        self.assertEqual(dict["id"], obj.id)
        self.assertEqual(dict["name"], obj.name)
        self.assertEqual(dict["school"], obj.school)
        self.assertEqual(dict["rank"], obj.rank)
        self.assertEqual(dict["created_at"], obj.created_at.isoformat())
        self.assertEqual(dict["updated_at"], obj.updated_at.isoformat())

    def test_save(self):
        """Tests for save() method"""

        obj = BaseModel()

        # test update_at datetime
        old_time = obj.updated_at
        time.sleep(2)
        obj.save()  # call save method
        new_time = obj.updated_at
        self.assertNotEqual(old_time, new_time)

        # check file serialization by .save()
        key = f"{type(obj).__name__}.{obj.id}"
        content = {key: obj.to_dict()}
        # check file existance
        self.assertTrue(os.path.isfile(FileStorage._FileStorage__file_path))
        with open(
            FileStorage._FileStorage__file_path, "r", encoding="utf-8"
        ) as file:
            self.assertEqual(len(file.read()), len(json.dumps(content)))
            file.seek(0)
            self.assertEqual(json.load(file), content)


if __name__ == "__main__":
    unittest.main()
