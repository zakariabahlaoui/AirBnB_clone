#!/usr/bin/python3
"""This module contains FileStorage class"""

import json
import os


class FileStorage:
    """
    This class is responsible for handling app storage, as well as storing
    objects to a file based storage (JSON)
    - serializes instances to a JSON file
    - deserializes JSON file to instances
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return objects dictionary"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in objects dictionary"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes objects dictionary to the JSON file"""
        with open(FileStorage.__file_path, "w", encoding="utf-8") as file:
            # make a dictionary that includes objects as dictionaries
            dict = {
                key: value.to_dict()
                for key, value in FileStorage.__objects.items()
            }
            # save the dictionary to the json file
            json.dump(dict, file)

    def reload(self):
        """Deserializes the JSON file to objects dictionary"""
        if not os.path.exists(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, "r", encoding="utf-8") as file:
            # retrieve a dictionary from our storage file
            # with object instances as dictionaries
            dict = json.load(file)

            # alter the retrieved dictionary values with object instances
            # using the corresponding class stored in __class__ attribute
            classes = self.get_app_classes()
            dict = {
                key: classes[value["__class__"]](**value)
                for key, value in dict.items()
            }
            FileStorage.__objects = dict

    def get_app_classes(self):
        """Get a dictionary that holds all app classes | names, references"""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        return {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review,
        }
