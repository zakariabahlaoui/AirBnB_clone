#!/usr/bin/python3
"""This module contains the BaseModel class representation"""

import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """BaseModel class representation,
    A base class for all other app classes (sub-classes)"""

    def __init__(self, *args, **kwargs):
        """
        Class constructor

        Args:
            *args: list of variable arguments
            **kwargs: dictionnay of arguments (key:values pairs)
        """
        if kwargs and kwargs is not None:  # not empty not None
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    # convert to datatime type
                    self.__dict__[key] = datetime.strptime(
                        value, "%Y-%m-%dT%H:%M:%S.%f"
                    )
                elif key != "__class__":  # other attributes except __class__
                    self.__dict__[key] = kwargs[key]
        else:  # kwargs not provided
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """The official string representation"""
        rep = f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
        return rep

    def save(self):
        """Updates the public instance attribute updated_at
        with the current datetime"""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Returns a dictionary containing all keys/values
        of __dict__ of an instance"""
        dict = self.__dict__.copy()
        # add some items to the dictionary
        dict["__class__"] = self.__class__.__name__
        dict["created_at"] = self.created_at.isoformat()
        dict["updated_at"] = self.updated_at.isoformat()
        return dict
