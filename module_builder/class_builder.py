from abc import ABCMeta, abstractmethod
from module_builder.type_finder import TypeFinder


#  abstract component class - defines the interface for composite objects
class Component(metaclass=ABCMeta):
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
    def write_files(self) -> str:
        pass


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


#  Director Class - instructs the builder what to build
class Director(object):
    def __init__(self, b):
        self._my_builder = b

    @property
    def my_builder(self):
        return self._my_builder

    def build_class(self, args):
        self.my_builder.add_class_name(args[0])
        self.my_builder.add_class_attributes(args[1])
        self.my_builder.add_class_methods(args[2])
        self.my_builder.add_relationships(args[3])


#  the Python Concrete builder - builds class data to write a python file
# code updated so that the Python Class created can be re-factored to the
# Composite Pattern
class PythonClassBuilder(AbstractClassBuilder):
    def __init__(self):
        self.new_class = PythonClass()

    def add_class_name(self, name):
        self.new_class.name = name

    def add_class_attributes(self, new_attributes):
        for an_attribute in new_attributes:
            new_a = Attribute(an_attribute.split(":")[0],
                              an_attribute.split(":")[1])
            self.new_class.add(new_a)
            new_a.parent = self.new_class

    def add_class_methods(self, new_methods):
        for a_method in new_methods:
            new_m = Method(a_method.split("(")[0],
                           a_method.split(")")[1],
                           a_method[
                           a_method.find("(") + 1:a_method.find(")")])
            self.new_class.add(new_m)
            new_m.parent = self.new_class

    def add_relationships(self, new_relationships):
        for a_relationship in new_relationships:
            rc = RelationshipCreator()
            rc.add_relationship(a_relationship, self.new_class)

    def get_class(self):
        return self.new_class


# composite class - contains the indivdual classes (replaces the Module Class)
class ModuleComposite(Component):
    def __init__(self) -> None:
        self._module_name = ""
        self._children = []

    @property
    def module_name(self):
        return self._module_name

    @property
    def children(self):
        return self._children

    # pre-defined function - not part of the composite pattern
    def create_module(self, new_module_name, new_classes):
        self._module_name = new_module_name.lower()
        for a_class in new_classes:
            self.add(a_class)

    # composite pattern - add component
    def add(self, component):
        self.children.append(component)
        component.parent = self

    # composite pattern - remove component
    def remove(self, component):
        self.children.remove(component)
        component.parent = None

    # composite pattern - is_composite
    def is_composite(self):
        return len(self.children) != 0

    # composite pattern - write data
    def write_files(self):
        folder_name = self.module_name
        my_files = []
        file_data = ""
        if self.is_composite():
            for child in self.children:
                file_data += child.write_files()
                file_name = child.name.lower() + ".py"
                my_files.append(tuple((file_name, file_data)))
        return [folder_name, my_files]


# Python Class - the product that the builder builds
# Class amended to become a component of the composite pattern
class PythonClass(Component):

    def __init__(self):
        self._name = ""
        self._children = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def children(self):
        return self._children

    def __str__(self):
        string = ""
        string += f"class {self.name}"
        if self.is_composite():
            for child in self.children:
                if isinstance(child, ExtendsRelationship):
                    string += f"({child.name})"
            string += ":\n\n\tdef __init__(self):\n"
            for child in self.children:
                if isinstance(child, Attribute):
                    string += child.write_files()
            for child in self.children:
                if isinstance(child, CompositeRelationship):
                    string += f"\t\tself.all_my_{child.name} = []\n"
            string += "\n"
            for child in self.children:
                if isinstance(child, Method):
                    string += child.write_files()
        return string

    def write_files(self):
        return self.__str__()

    def add(self, component):
        self.children.append(component)

    def remove(self, component):
        self.children.remove(component)

    def is_composite(self):
        return len(self.children) != 0


class Attribute(Component):
    def __init__(self, new_name, new_type):
        self._name = new_name.replace(" ", "")
        self._type = TypeFinder.find_type(new_type)

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    def __str__(self):
        string_dict = {"str": f"\t\t"
                       f"self.{self.name}: {self.type} = \"\"  # ToDo\n",
                       "int": f"\t\t"
                       f"self.{self.name}: {self.type} = 1  # ToDo\n",
                       "list": f"\t\t"
                       f"self.{self.name}: {self.type} = []  # ToDo\n",
                       }
        return string_dict.get(self.type,
                               f"\t\tself.{self.name} = None  # ToDo\n")

    def is_composite(self):
        return False

    def write_files(self):
        return self.__str__()


class Method(Component):

    def __init__(self, new_name, new_return, new_input):
        self._name = new_name.replace("()", "").replace(" ", "")
        self._input = new_input.replace("()", "")
        self._return_type = TypeFinder.find_type(new_return)

    @property
    def name(self):
        return self._name

    @property
    def input(self):
        return self._input

    @property
    def return_type(self):
        return self._return_type

    def __str__(self):
        if self.input != "":
            return f"\tdef {self.name}" \
                f"(self, {self.input}) ->{self.return_type}:\n" \
                f"\t\t# ToDo\n        pass\n\n"
        else:
            return f"\tdef {self.name}" \
                f"(self) ->{self.return_type}:\n\t\t" \
                f"# ToDo\n\t\tpass\n\n"

    def is_composite(self):
        return False

    def write_files(self):
        return self.__str__()


class Creator(metaclass=ABCMeta):
    @abstractmethod
    def factory_method(self, new_type):
        pass


# Factory Pattern - Just a bonus that made this code easier to
# re-factor into the other patterns by refactorng how my
# relationships were built, but I already used
# a creational pattern with the builder Method
class RelationshipCreator:

    def factory_method(self, new_type):
        if new_type[0] == "comp":
            return CompositeRelationship(new_type)
        elif new_type[0] == "assos":
            return AssociationRelationship(new_type)
        elif new_type[0] == "extends":
            return ExtendsRelationship(new_type)

    def add_relationship(self, new_type, parent):
        product = self.factory_method(new_type)
        product.add_relationship(parent)


class Relationship(Component):

    def __init__(self, new_type):
        self.__parent = None
        self.__name = new_type[1]
        self.__type = None

    @property
    def parent(self):
        return self.__parent

    @property
    def name(self):
        return self.__name

    @property
    def type(self):
        return self.type

    @type.setter
    def type(self, new_type):
        self.__type = new_type

    def return_type(self):
        return self.type

    def write_files(self):
        return self.name

    def is_composite(self):
        return False

    def add_relationship(self, parent):
        pass


class CompositeRelationship(Relationship):
    def __init__(self, new_type):
        super().__init__(new_type)

    def add_relationship(self, parent):
        self.__name = self.name.lower()
        self.__name += "s"
        self.type = "comp"
        parent.children.append(self)


class AssociationRelationship(Relationship):
    def __init__(self, new_type):
        super().__init__(new_type)

    def add_relationship(self, parent):
        parent.children.append(self)
        self.type = "assos"


class ExtendsRelationship(Relationship):
    def __init__(self, new_type):
        super().__init__(new_type)

    def add_relationship(self, parent):
        parent.children.append(self)
        self.type = "extends"
