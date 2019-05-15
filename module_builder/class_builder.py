from module_builder.method import Method
from module_builder.attribute import Attribute
from module_builder.relationship import Relationship
from abc import ABCMeta, abstractmethod


#  Abstract builder - defines the interface for the concrete builders
class AbstractClassBuilder(metaclass=ABCMeta):
    @abstractmethod
    def add_class_name(self, name):
        pass

    @abstractmethod
    def add_class_attributes(self, new_attributes):
        pass

    @abstractmethod
    def add_class_methods(self, new_methods):
        pass

    @abstractmethod
    def add_relationships(self, relationships):
        pass


#  the Python Concrete builder - builds class data to write a python file
class PythonClassBuilder(AbstractClassBuilder):
    def __init__(self):
        self.new_class = PythonClass()

    def add_class_name(self, name):
        self.new_class.name = name

    def add_class_attributes(self, new_attributes):
        for an_attribute in new_attributes:
            new_a = Attribute(an_attribute.split(":")[0],
                              an_attribute.split(":")[1])
            self.new_class.all_my_attributes.append(new_a)

    def add_class_methods(self, new_methods):
        for a_method in new_methods:
            new_m = Method(a_method.split("(")[0],
                           a_method.split(")")[1],
                           a_method[
                           a_method.find("(") + 1:a_method.find(")")])
            self.new_class.all_my_methods.append(new_m)

    def add_relationships(self, relationships):
        for a_relationship in relationships:
            new_relationship = Relationship(a_relationship, self)
            new_relationship.add_relationship()

    def get_class(self):
        return self.new_class


#  Director Class - instructs the builder what to build
class Director(object):
    def __init__(self, b):
        self.my_builder = b

    def build_class(self, args):
        self.my_builder.add_class_name(args[0])
        self.my_builder.add_class_attributes(args[1])
        self.my_builder.add_class_methods(args[2])
        self.my_builder.add_relationships(args[3])


#  Python Class - the product that the builder builds
class PythonClass:

    def __init__(self):
        self.name = ""
        self.all_my_attributes = []
        self.all_my_methods = []
        self.all_my_parent_classes = []
        self.all_my_composite_classes = []
        self.all_my_associated_classes = []

    def __str__(self):
        string = ""
        string += f"class {self.name}"
        if len(self.all_my_parent_classes) > 0:
            for a_class in self.all_my_parent_classes:
                string += f"({a_class})"
        string += ":\n\n    def __init__(self):\n"
        for x in self.all_my_attributes:
            string += f"{x}"
        if len(self.all_my_composite_classes) > 0:
            for a_class in self.all_my_composite_classes:
                string += f"        self.all_my_{a_class} = []\n"
        string += "\n"
        for x in self.all_my_methods:
            string += f"{x}"
        return string

    def print_class(self):
        return self.__str__()
