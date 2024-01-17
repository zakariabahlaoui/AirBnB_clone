#!/usr/bin/python3
"""Unittests for console.py"""

import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models.engine.file_storage import FileStorage
from models import storage
import os

from models.user import User


class TestHBNBCommand(unittest.TestCase):
    """Tests HBNBCommand console interpreter class"""

    classes = storage.get_app_classes()

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

    def test_help(self):
        """Test help command"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("help")

        commands = [
            "EOF",
            "all",
            "count",
            "create",
            "destroy",
            "help",
            "quit",
            "show",
            "update",
        ]
        # help command output
        result = f.getvalue()
        # Check if all commands exist in the result of help command
        all_commands_exist = all(command in result for command in commands)
        self.assertTrue(all_commands_exist)

    def test_do_quit(self):
        """Test quit command"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("quit")
        output = f.getvalue()
        self.assertEqual("", output)
        # extra arguments
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("quit nonsense")
        output = f.getvalue()
        self.assertEqual("", output)

    def test_do_EOF(self):
        """Test EOF commmand"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("EOF")
        output = f.getvalue()
        self.assertEqual("\n", output)

    def test_emptyline(self):
        """Test emptyline"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("\n")
        output = f.getvalue()
        self.assertEqual("", output)

        # with preceding tabs/spaces
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("       \n")
        output = f.getvalue()
        self.assertEqual("", output)

    def test_do_create(self):
        """Test create command on all classes"""
        # test for all classes
        for classname in self.classes:
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {classname}")
            id = f.getvalue()[:-1]
            self.assertTrue(len(id) > 0)
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd(f"show {classname} {id}")
            self.assertTrue(id in f.getvalue())

        # test with no args
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        # test with invalid class
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create MarsClass")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

    def test_do_show(self):
        """Test show command on all classes"""
        # with all classes
        for classname in self.classes:
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {classname}")
            id = f.getvalue()[:-1]
            self.assertTrue(len(id) > 0)

            # test normal command format
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd(f"show {classname} {id}")
            output = f.getvalue()[:-1]
            self.assertIn(id, output)

            # test method syntax
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd(f'{classname}.show("{id}")')
            output = f.getvalue()
            self.assertTrue(id in output)

            # errors
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd("show")
            output = f.getvalue()[:-1]
            self.assertEqual(output, "** class name missing **")

            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd("show MarsClass")
            output = f.getvalue()[:-1]
            self.assertEqual(output, "** class doesn't exist **")

            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd("show User")
            output = f.getvalue()[:-1]
            self.assertEqual(output, "** instance id missing **")

            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd("show User invalid_id")
            output = f.getvalue()[:-1]
            self.assertEqual(output, "** no instance found **")

            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd(f'MoonClass.show("{id}")')
            output = f.getvalue()[:-1]
            self.assertEqual(output, "** class doesn't exist **")

            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd(f'{classname}.show("")')
            output = f.getvalue()[:-1]
            self.assertEqual(output, "** instance id missing **")

            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd(f'{classname}.show("invalid-id")')
            output = f.getvalue()[:-1]
            self.assertEqual(output, "** no instance found **")

    def test_do_destroy(self):
        """Test destroy command on all classes"""
        for classname in self.classes:
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {classname}")
            id = f.getvalue()[:-1]
            self.assertTrue(len(id) > 0)

            # try with normal syntax
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd(f"destroy {classname} {id}")
            output = f.getvalue()[:-1]
            self.assertTrue(output == "")

            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd("all")
            self.assertFalse(id in f.getvalue())

            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {classname}")
            id = f.getvalue()[:-1]
            self.assertTrue(len(id) > 0)

            # with method syntax
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd(f'{classname}.destroy("{id}")')
            s = f.getvalue()[:-1]
            self.assertTrue(len(s) == 0)

            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd("all")
            self.assertFalse(id in f.getvalue())

            # errors
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd("destroy")
            output = f.getvalue()[:-1]
            self.assertEqual(output, "** class name missing **")

            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd("destroy MoonClass")
            output = f.getvalue()[:-1]
            self.assertEqual(output, "** class doesn't exist **")

            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd("destroy Amenity")
            output = f.getvalue()[:-1]
            self.assertEqual(output, "** instance id missing **")

            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd("destroy Amenity invalid-id")
            output = f.getvalue()[:-1]
            self.assertEqual(output, "** no instance found **")

    def test_do_all(self):
        """Test all command for all classes"""
        for classname in self.classes:
            # create instance of target class
            obj = self.classes[classname]()
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd("all")
            output = f.getvalue()[:-1]
            self.assertTrue(len(output) > 0)
            self.assertIn(obj.id, output)

            # all with argument
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd(f"all {classname}")
            output = f.getvalue()[:-1]
            self.assertTrue(len(output) > 0)
            self.assertIn(obj.id, output)

            # using syntax method
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd(f"{classname}.all()")
            output = f.getvalue()[:-1]
            self.assertTrue(len(output) > 0)
            self.assertIn(obj.id, output)

            # errors
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd("all MarsClass")
            output = f.getvalue()[:-1]
            self.assertEqual(output, "** class doesn't exist **")

            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd("MarsClass.all()")
            output = f.getvalue()[:-1]
            self.assertEqual(output, "** class doesn't exist **")

    def test_count_all(self):
        """Test count command on all classes."""
        for classname in self.classes:
            # create 3 instances
            for i in range(3):
                obj = self.classes[classname]()
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd(f"count {classname}")
            output = f.getvalue()[:-1]
            self.assertTrue(len(output) > 0)
            self.assertEqual(output, "3")
            # method syntax
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd(f"{classname}.count()")
            output = f.getvalue()[:-1]
            self.assertTrue(len(output) > 0)
            self.assertEqual(output, "3")

            # errors
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd("count")
            output = f.getvalue()[:-1]
            self.assertEqual(output, "** class name missing **")
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd("count MoonClass")
            output = f.getvalue()[:-1]
            self.assertEqual(output, "** class doesn't exist **")
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd("MoonClass.count()")
            output = f.getvalue()[:-1]
            self.assertEqual(output, "** class doesn't exist **")

    def test_do_update(self):
        """Test update command"""
        obj = User()
        # update user
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(f"update User {obj.id} school Holberthon")
        output = f.getvalue()[:-1]
        self.assertTrue(output == "")
        # check update with show
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(f"show User {obj.id}")
        output = f.getvalue()[:-1]
        self.assertIn("Holberthon", output)

        # with method syntax
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(f"User.update({obj.id}, school, 1337)")
        output = f.getvalue()[:-1]
        self.assertTrue(output == "")
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(f"show User {obj.id}")
        output = f.getvalue()[:-1]
        self.assertIn("1337", output)

        # try update with dictionary
        obj.name = ""
        obj.job = ""
        with patch("sys.stdout", new=StringIO()) as f:
            dict_str = '{"name": "Julien", "job": "CEO"}'
            HBNBCommand().onecmd(f'User.update("{obj.id}", {dict_str})')
        output = f.getvalue()[:-1]
        self.assertTrue(output == "")
        self.assertEqual(obj.name, "Julien")
        self.assertEqual(obj.job, "CEO")

        # errors
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update")
        output = f.getvalue()[:-1]
        self.assertEqual(output, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update BlueMoon")
        output = f.getvalue()[:-1]
        self.assertEqual(output, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update User")
        output = f.getvalue()[:-1]
        self.assertEqual(output, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update User invalid-id")
        output = f.getvalue()[:-1]
        self.assertEqual(output, "** no instance found **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'update User {obj.id}')
        output = f.getvalue()[:-1]
        self.assertEqual(output, "** attribute name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'update User {obj.id} name')
        output = f.getvalue()[:-1]
        self.assertEqual(output, "** value missing **")

        # method syntax errors
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BlueMoon.update()")
        output = f.getvalue()[:-1]
        self.assertEqual(output, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("User.update()")
        output = f.getvalue()[:-1]
        self.assertEqual(output, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("User.update(invalid-id)")
        output = f.getvalue()[:-1]
        self.assertEqual(output, "** no instance found **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'User.update("{obj.id}")')
        output = f.getvalue()[:-1]
        self.assertEqual(output, "** attribute name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'User.update("{obj.id}", "name")')
        output = f.getvalue()[:-1]
        self.assertEqual(output, "** value missing **")

    def test_update_with_dict(self):
        """Test update_with_dict function"""
        obj = User()
        obj.name = ""
        obj.job = ""
        dict_str = '{"name": "Julien", "job": "CEO"}'
        # call update method
        HBNBCommand.update_with_dict(self, "User", obj.id, dict_str)
        self.assertEqual(obj.name, "Julien")
        self.assertEqual(obj.job, "CEO")

    def test_is_dictionary(self):
        """Test is_dictionary function"""
        dict_str_valid = '{"name": "Julien", "school": "Holberthon"}'
        self.assertTrue(HBNBCommand.is_dictionary(self, dict_str_valid))
        dict_str_wrong = '{"name": "Julien" + "school": Holberthon"]'
        self.assertFalse(HBNBCommand.is_dictionary(self, dict_str_wrong))

    def test_convert_command(self):
        """Test convert_command function"""
        command = "User.User.show(id)"
        result = HBNBCommand.convert_command(self, command)
        self.assertEqual(result, "show User id")

    def test_get_attribute_value(self):
        """Test get_attribute_value function"""
        args = list = ["arg0", "arg1", "arg2", "arg3"]
        result = HBNBCommand.get_attribute_value(self, args)
        self.assertEqual(result, "arg3")
        args = list = ["arg0", "arg1", "arg2", '"arg3']
        result = HBNBCommand.get_attribute_value(self, args)
        self.assertEqual(result, '"arg3')


if __name__ == "__main__":
    unittest.main()
