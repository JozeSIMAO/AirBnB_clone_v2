#!/usr/bin/python3
"""Defines a class HBNBCommand, entry point of the command interpreter"""
import cmd
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State


class HBNBCommand(cmd.Cmd):
    """Represents the the HBNBCommand class"""
    prompt = '(hbnb) '

    __classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "Place": Place,
        "Amenity": Amenity,
        "City": City,
        "Review": Review
    }

    def __init__(self):
        super().__init__()
        self.file_storage = FileStorage()

    def do_quit(self, arg):
        """Exits the program if (quit) is input"""
        return True

    def do_EOF(self, arg):
        """Exits the program if (EOF) is input"""
        return True

    def emptyline(self):
        """Does nothing"""
        pass

    def do_create(self, arg):
        """Creates a new instance of a class, saves it, and prints the id"""
        # Split the input string using shlex for proper handling of quotes
        args = arg.split()

        if not args:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            class_name = args[0]
            params = {}

            i = 1
            while i < len(args):
                param = args[i]
                try:
                    key, value = param.split('=')
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1].replace('_', ' ')
                        value = value.replace('\\"', '"')
                    elif '.' in value:
                        value = float(value)
                    else:
                        value = int(value)

                    params[key] = value
                    i += 1  # Increment to move to the next argument
                except ValueError:
                    print(f"Skipping invalid parameter: {param}")
                    i += 1  # Skip to the next argument

            file_storage = FileStorage()
            new_instance = HBNBCommand.__classes[class_name](**params)
            print(new_instance.id)
            file_storage.new(new_instance)
            file_storage.save()

    def do_show(self, arg):
        """Prints the string representation of an instance"""
        args = arg.split()

        if not args:
            print("** class name missing **")
            return
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:

            class_name = args[0]
            instance_id = args[1]
            file_storage = FileStorage()
            instance = file_storage.all().get(f"{class_name}.{instance_id}")
            if instance:
                print(instance)
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        if not arg:
            print("**class name missing **")
            return

        args = arg.split()
        class_name = args[0]
        file_storage = FileStorage()

        if class_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        instances = file_storage.all()
        key = f"{class_name}.{instance_id}"

        if key in instances:
            del instances[key]
            file_storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """Prints all string representations of instances"""
        file_storage = FileStorage()
        file_storage.classes = {
            "BaseModel": BaseModel,
            "User": User,
            "Place": Place,
            "Review": Review,
            "State": State,
            "Amenity": Amenity,
        }
        file_storage.reload()
        instances = file_storage.all()
        args = arg.split()

        if not arg:
            print([str(instance) for instance in file_storage.all().values()])
        elif args:
            class_name = args[0]
            if class_name in file_storage.classes:
                object_list = [str(instance) for instance in instances.values()
                               if instance.__class__.__name__ == class_name]
                if object_list:
                    print(object_list)
                else:
                    print("[]")
            else:
                print("** class doesn't exist **")

    def do_update(self, arg):
        """Updates an instance's attribute"""
        args = arg.split()
        file_storage = FileStorage()
        instance_id = args[1]

        if not arg:
            print("** class name missing **")
        else:
            class_name = args[0]
            if len(args) < 2:
                print("** instance id missing **")
            elif f"{class_name}.{instance_id}" not in file_storage.all():
                print("** no instance found **")
            elif len(args) < 3:
                print("** attribute name missing **")
            elif len(args) < 4:
                print("** value missing **")
            else:
                instance_id = args[1]
                attr_name = args[2]
                attr_value = args[3]
                instance = file_storage.all().get(f"{class_name}.{instance_id}")

                if instance:
                    setattr(instance, attr_name, attr_value)
                    instance.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
