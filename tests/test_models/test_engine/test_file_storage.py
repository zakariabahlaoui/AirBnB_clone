#!/usr/bin/python3
"""Unittests for models/engine/file_storage.py"""

import unittest
from models.engine.file_storage import FileStorage
from models.user import User
from models import storage
import json
import os


class TestFileStorage(unittest.TestCase):
    """Contains test cases for the FileStorage class"""

    @classmethod
    def setUpClass(cls):
        """Executes once before running tests"""
        # resets storage data
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            # remove json file
            os.remove(FileStorage._FileStorage__file_path)

    def tearDown(self):
        """Runs after each test"""
        # resets storage data
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            # remove json file
            os.remove(FileStorage._FileStorage__file_path)

    def test_init(self):
        """Test the constructor"""
        self.assertEqual(type(storage).__name__, "FileStorage")
        # test initalize with arguments
        with self.assertRaises(TypeError) as e:
            obj = FileStorage(2023, 2024)
        self.assertEqual(str(e.exception), "FileStorage() takes no arguments")
        # check attributes
        self.assertTrue(hasattr(FileStorage, "_FileStorage__file_path"))
        self.assertTrue(hasattr(FileStorage, "_FileStorage__objects"))
        self.assertEqual(
            getattr(FileStorage, "_FileStorage__objects"), {}
        )

    def test_all(self):
        """Test all() method"""
        FileStorage._FileStorage__objects = {}
        self.assertEqual(storage.all(), {})

        # add object and check
        obj = User()
        storage.new(obj)
        key = f"{type(obj).__name__}.{obj.id}"
        self.assertEqual(storage.all()[key], obj)

    def test_new(self):
        """Tests new() method"""

        # add new object to storage
        obj = User()
        storage.new(obj)
        key = f"{type(obj).__name__}.{obj.id}"
        self.assertTrue(key in FileStorage._FileStorage__objects)

        # no argument passed
        with self.assertRaises(TypeError) as e:
            obj = User()
            storage.new()
        # too many argument passed
        with self.assertRaises(TypeError) as e:
            obj = User()
            storage.new(obj, 2024)

    def test_save(self):
        """Tests save() method"""
        obj = User()
        storage.new(obj)
        key = f"{type(obj).__name__}.{obj.id}"
        storage.save()
        # check file existance
        self.assertTrue(os.path.isfile(FileStorage._FileStorage__file_path))
        # check file serialization
        content = {key: obj.to_dict()}
        with open(
            FileStorage._FileStorage__file_path, "r", encoding="utf-8"
        ) as f:
            self.assertEqual(len(f.read()), len(json.dumps(content)))
            f.seek(0)
            self.assertEqual(json.load(f), content)

    def test_save_too_many_args(self):
        """Tests save() with too many arguments"""
        with self.assertRaises(TypeError) as e:
            FileStorage.save(self, 2024)

    def test_reload(self):
        """Test reload() method"""
        storage.reload()
        self.assertEqual(FileStorage._FileStorage__objects, {})
        obj = User()
        storage.new(obj)
        storage.save()
        storage.reload()
        key = f"{type(obj).__name__}.{obj.id}"
        self.assertEqual(obj.to_dict(), storage.all()[key].to_dict())


if __name__ == "__main__":
    unittest.main()
