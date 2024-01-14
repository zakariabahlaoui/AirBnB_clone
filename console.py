#!/usr/bin/python3
"""This module contains the command interpreter class"""

import cmd
import re
from models import storage


class HBNBCommand(cmd.Cmd):
    """Interpreter's command processor class"""

    prompt = "(hbnb) "

    def do_quit(self, args):
        """Exit the program"""
        return True

    def do_EOF(self, args):
        """Handle end of file character"""
        print()  # new line
        return True  # quit

    def emptyline(self):
        """Handle empty line + ENTER"""
        pass  # do nothing

    def do_create(self, args):
        """Creates a new instance of an object and saves it
        Usage: create <class_name>"""
        classes = storage.get_app_classes()
        if args == "" or args is None:
            print("** class name missing **")
        elif args not in classes:
            print("** class doesn't exist **")
        else:
            obj = classes[args]()  # initialize new object of the corresponding class
            obj.save()
            print(obj.id)

    def do_show(self, args):
        """Prints the string representation of an obj based on the class name and id
        Usage: show <class_name> <object_id>"""
        if args == "" or args is None:
            print("** class name missing **")
            return

        args_list = args.split(" ")
        classes = storage.get_app_classes()
        if args_list[0] not in classes:
            print("** class doesn't exist **")
            return

        if len(args_list) < 2:  # only one argument provided
            print("** instance id missing **")
            return

        key = f"{args_list[0]}.{args_list[1]}"
        if key in storage.all():
            print(storage.all()[key])
        else:
            print("** no instance found **")

    def do_destroy(self, args):
        """Deletes an instance based on the class name and id
        Usage: destroy <class_name> <object_id>"""
        if args == "" or args is None:
            print("** class name missing **")
            return

        args_list = args.split(" ")
        classes = storage.get_app_classes()
        if args_list[0] not in classes:
            print("** class doesn't exist **")
            return

        if len(args_list) < 2:  # only one argument provided
            print("** instance id missing **")
            return

        key = f"{args_list[0]}.{args_list[1]}"
        if key in storage.all():
            # remove instance from objects dictionary
            del storage.all()[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, args):
        """Prints all string representation of all instances based or not on the class name
        Usage: all OR all <class_name>"""
        if args == "" or args is None:  # command = all
            # print all objects (any type)
            obj_list = [str(object) for object in storage.all().values()]
            print(obj_list)
            return

        args_list = args.split(" ")
        classes = storage.get_app_classes()
        if args_list[0] not in classes:
            print("** class doesn't exist **")
            return

        # print all instances of the class provided
        obj_list = [
                str(object)
                for object in storage.all().values()
                if type(object) == classes[args_list[0]]
                ]
        print(obj_list)

    def do_update(self, args):
        """Updates an instance based on the class name and id by adding or updating attribute
        Usage: update <class_name> <id> <attribute_name> "<attribute_value>"""
        if args == "" or args is None:
            print("** class name missing **")
            return

        args_list = args.split(" ")
        classes = storage.get_app_classes()
        if args_list[0] not in classes:
            print("** class doesn't exist **")
            return

        if len(args_list) < 2:  # only one argument provided
            print("** instance id missing **")
            return

        key = f"{args_list[0]}.{args_list[1]}"  # <class_name>.id
        if key in storage.all():
            if len(args_list) < 3:
                print("** attribute name missing **")
            elif len(args_list) < 4:
                print("** value missing **")
            else:  # all the required arguments exist
                # update the object attribute value (with valid type)
                obj = storage.all()[key]
                attr = args_list[2]
                # cast the value before assign it to the object
                attr_type = type(getattr(obj, attr)) if hasattr(obj, attr) else str
                value = attr_type(self.get_attribute_value(args_list))
                setattr(obj, attr, value)
                obj.save()
        else:
            print("** no instance found **")

    def get_attribute_value(self, args_list):
        """
        Get full attribute value

        Args:
            args_list (list): list of interpreter command's arguments
        Returns:
            str - valid attribute value
        """

        value = args_list[3]  # attribute value

        # check if attribute value is a multi-word string!
        # ex. "my attribute value"
        if value.startswith('"'):
            # join arguments starting from argument at index 3
            value = " ".join(args_list[3:])
            # search using regex for text inside double quotes
            match = re.search(r'"([^"]*)"', value)
            # get the text inside double quotes if there is a match
            # otherwise, get the first word as value attribute
            value = match.group(1) if match else args_list[3]

        return value


if __name__ == "__main__":
    HBNBCommand().cmdloop()

