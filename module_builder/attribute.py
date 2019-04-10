from .type_finder import TypeFinder


class Attribute:

    def __init__(self, new_name, new_type):
        self.name = new_name.replace(" ", "")
        self.type = TypeFinder.find_type(new_type)

    def __str__(self):
        string_dict = {"str": f"        self.{self.name}: {self.type} = \"\"  # ToDo\n",
                       "int": f"        self.{self.name}: {self.type} = 1  # ToDo\n",
                       "list": f"        self.{self.name}: {self.type} = []  # ToDo\n",
                       }
        return string_dict.get(self.type, f"        self.{self.name} = None  # ToDo\n")
