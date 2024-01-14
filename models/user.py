#!/usr/bin/python3
"""This module contains the User class representation"""

from models.base_model import BaseModel


class User(BaseModel):
    """User class representation"""

    email = ""
    password = ""
    first_name = ""
    last_name = ""
