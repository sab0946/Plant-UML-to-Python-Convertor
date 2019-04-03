class Attribute:

    """define the attributes of a class
    >>> a = Attribute('first_attribute', 'string')
    >>> print(a.name)
    first_attribute
    >>> print(a.type)
    str
    """

    def __init__(self, new_name, new_type):
        self.name = new_name.replace(" ", "")
        self.type = self.find_type(new_type)

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

    @staticmethod
    def find_type(new_type):
        if "string" in new_type:
            return "str"
        elif "number" in new_type:
            return "int"
        elif "list" in new_type:
            return "list"
        elif "tuple" in new_type:
            return "tuple"
        else:
            return ""


if __name__ == "__main__":
    from doctest import testmod
    testmod()
