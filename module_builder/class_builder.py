from .method import Method
from .attribute import Attribute
from .relationship import Relationship


class ClassBuilder:

    """Create an instance of the object ClassBuilder
    that contains a list of the objects attributes, methods
    and relationships"""

    def __init__(self):
        self.name = ""
        self.all_my_attributes = []
        self.all_my_methods = []
        self.all_my_parent_classes = []
        self.all_my_composite_classes = []
        self.all_my_associated_classes = []

    def add_class_attributes(self, new_attributes):
        for an_attribute in new_attributes:
            new_a = Attribute(an_attribute.split(":")[0],
                              an_attribute.split(":")[1])
            self.all_my_attributes.append(new_a)

    def add_class_methods(self, new_methods):
        for a_method in new_methods:
            new_m = Method(a_method.split("(")[0],
                           a_method.split(")")[1],
                           a_method[a_method.find("(")
                                    + 1:a_method.find(")")])
            self.all_my_methods.append(new_m)

    def add_relationships(self, new_relationships):
        for a_relationship in new_relationships:
            if "extends" in a_relationship:
                new_relationship = Relationship(a_relationship)
                self.all_my_parent_classes.append(new_relationship)
            elif "comp" in a_relationship:
                new_relationship = Relationship(a_relationship)
                self.all_my_composite_classes.append(new_relationship)
            elif "assos" in a_relationship:
                new_relationship = Relationship(a_relationship)
                self.all_my_associated_classes.append(new_relationship)

    def build_class(
            self, new_name, new_attributes, new_methods, new_relationships):
        self.name = new_name
        self.add_class_attributes(new_attributes)
        self.add_class_methods(new_methods)
        self.add_relationships(new_relationships)

    def print_class(self):
        string = ""
        string += f"class {self.name}"
        if len(self.all_my_parent_classes) > 0:
            for a_class in self.all_my_parent_classes:
                string += f"({a_class})"
        string += ":\n"
        string += "\n    def __init__(self):\n"
        for x in self.all_my_attributes:
            string += f"{x}"
        if len(self.all_my_composite_classes) > 0:
            for a_class in self.all_my_composite_classes:
                string += f"        self.all_my_{a_class} = []\n"
        string += "\n"
        for x in self.all_my_methods:
            string += f"{x}"
        return string
