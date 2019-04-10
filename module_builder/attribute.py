from .type_finder import TypeFinder

class Attribute:

    """define the attributes of a class"""

    def __init__(self, new_name, new_type):
        self.name = new_name.replace(" ", "")
        self.type = TypeFinder.find_type(new_type)

    def __str__(self):
        if "str" in self.type:
            return f"        self.{self.name}: {self.type} = \"\"  # ToDo\n"
        elif "int" in self.type:
            return f"        self.{self.name}: {self.type} = 1  # ToDo\n"
        elif "list" in self.type:
            return f"        self.{self.name}: {self.type} = []  # ToDo\n"
        elif "tuple" in self.type:
            return f"        self.{self.name}: {self.type} = ()  # ToDo\n"
        else:
            return f"        self.{self.name} = None  # ToDo\n"
