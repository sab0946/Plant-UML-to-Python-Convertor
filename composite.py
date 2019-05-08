from .method import Method
from .attribute import Attribute
from .relationship import Relationship
from abc import ABCMeta, abstractmethod


#  abstract component class - defines the interface for the composite objects
class ProgramComponent(metaclass=ABCMeta):

    @property
    def parent(self) -> object:
        return self._parent

    @parent.setter
    def parent(self, parent: object):
        self._parent = parent

    def add(self, component: object) -> None:
        pass

    def remove(self, component: object) -> None:
        pass

    def is_composite(self) -> bool:
        return False

    @abstractmethod
    def write_data(self) -> str:
        pass


#  composite class - contains individual classes
class ModuleComposite(ProgramComponent):
    def __init__(self) -> None:
        self.module_name = ""
        self.__all_my_classes= []

    # pre-defined function - not part of composite pattern
    def create_module(self, new_module_name, new_classes):
        self.module_name = new_module_name.lower()
        for a_class in new_classes:
            self.add(a_class)

    # composite pattern - add component
    def add(self, component=object):
        self.__all_my_classes.append(object)
        object.parent = self

    def remove(self, component=object):
        self.__all_my_classes.remove(object)
        object.parent = None

    def is_composite(self):
        return True

    def write_data(self):
        folder_name = self.module_name
        my_files = []
        for a_class in self.__all_my_classes:
            file_data = ""
            file_data += a_class.write_data()
            file_name = a_class.name.lower() + ".py"
            my_files.append(tuple((file_name, file_data)))
        return (folder_name, my_files)


# class in program - forms the component of the design pattern
class ClassComponent(ProgramComponent):
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
                           a_method[
                           a_method.find("(") + 1:a_method.find(")")])
            self.all_my_methods.append(new_m)

    def add_relationships(self, new_relationships):
        for a_relationship in new_relationships:
            new_relationship = Relationship(a_relationship, self)
            new_relationship.add_relationship()

    def build_class(self, args):
        self.name = args[0]
        self.add_class_attributes(args[1])
        self.add_class_methods(args[2])
        self.add_relationships(args[3])

    def write_data(self):
        return self.__str__()

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


