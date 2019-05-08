from module_builder.type_finder import TypeFinder
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
        self.children = []

    # pre-defined function - not part of composite pattern
    def create_module(self, new_module_name, new_classes):
        self.module_name = new_module_name.lower()
        for a_class in new_classes:
            self.add(a_class)

    # composite pattern - add component
    def add(self, component):
        self.children.append(component)
        component.parent = self

    def remove(self, component):
        self.children.remove(component)
        component.parent = None

    def is_composite(self):
        return True

    def write_data(self):
        folder_name = self.module_name
        my_files = []
        file_data = ""
        if self.is_composite():
            for child in self.children:
                file_data += child.write_data()
                file_name = child.name.lower() + ".py"
                my_files.append(tuple((file_name, file_data)))
        return [folder_name, my_files]


class AbstractBuilder(metaclass=ABCMeta):
    @abstractmethod
    def add_class_attributes(self, new_attributes):
        pass

    @abstractmethod
    def add_class_methods(self, new_methods):
        pass

    @abstractmethod
    def add_relationships(self, relationships):
        pass


class PythonClassBuilder(AbstractBuilder):
    def __init__(self, a_name):
        self.new_class = ClassComponent(a_name)

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
        print(self.new_class.name)
        return self.new_class


class ClassDirector(object):
    def __init__(self, b):
        self.my_builder = b

    def build_class(self, args):
        self.my_builder.add_class_attributes(args[1])
        self.my_builder.add_class_methods(args[2])
        self.my_builder.add_relationships(args[3])


# class in program - forms the component of the design pattern
class ClassComponent(ProgramComponent):
    def __init__(self, a_name):
        self.name = a_name
        self.children = []

    def __str__(self):
        string = ""
        string += f"class {self.name}"
        for child in self.children:
            if isinstance(child, ExtendsRelationship):
                string += f"({child.name})"
        string += ":\n\n    def __init__(self):\n"
        for child in self.children:
            if isinstance(child, Attribute):
                string += child.write_data()
        for child in self.children:
            if isinstance(child, CompositeRelationship):
                string += f"        self.all_my_{child.name} = []\n"
        string += "\n"
        for child in self.children:
            if isinstance(child, Method):
                string += child.write_data()
        return string

    # composite pattern code

    def write_data(self):
        return self.__str__()

    def add(self, component):
        self.children.append(component)

    def remove(self, component):
        self.children.remove(component)

    def is_composite(self):
        return True


class Attribute(ProgramComponent):
    def __init__(self, new_name, new_type):
        self.name = new_name.replace(" ", "")
        self.type = TypeFinder.find_type(new_type)

    def __str__(self):
        string_dict = {"str": f"        "
        f"self.{self.name}: {self.type} = \"\"  # ToDo\n",
                       "int": f"        "
                       f"self.{self.name}: {self.type} = 1  # ToDo\n",
                       "list": f"        "
                       f"self.{self.name}: {self.type} = []  # ToDo\n",
                       }
        return string_dict.get(self.type,
                               f"        self.{self.name} = None  # ToDo\n")

    def is_composite(self):
        return False

    def write_data(self):
        return self.__str__()


class Method(ProgramComponent):

    def __init__(self, new_name, new_return, new_input):
        self.name = new_name.replace("()", "").replace(" ", "")
        self.input = new_input.replace("()", "")
        self.return_type = TypeFinder.find_type(new_return)

    def __str__(self):
        if self.input != "":
            return f"    def {self.name}" \
                f"(self, {self.input}) ->{self.return_type}:\n " \
                f"       # ToDo\n        pass\n\n"
        else:
            return f"    def {self.name}" \
                f"(self) ->{self.return_type}:\n        " \
                f"# ToDo\n        pass\n\n"

    def is_composite(self):
        return False

    def write_data(self):
        return self.__str__()


class Creator(metaclass=ABCMeta):
    @abstractmethod
    def factory_method(self, new_type):
        pass


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


class Relationship(ProgramComponent):

    def __init__(self, new_type):
        self.parent = None
        self.name = new_type[1]
        self.type = new_type[0]

    def return_type(self):
        return self.type

    def write_data(self):
        return self.name

    def is_composite(self):
        return False

    def add_relationship(self, parent):
        pass


class CompositeRelationship(Relationship):
    def add_relationship(self, parent):
        self.name = self.name.lower()
        self.name += "s"
        parent.children.append(self)


class AssociationRelationship(Relationship):
    def add_relationship(self, parent):
        parent.children.append(self)


class ExtendsRelationship(Relationship):
    def add_relationship(self, parent):
        parent.children.append(self)


if __name__ == "__main__":
    simple = Method("test","test","string")
    print("single component")
    print(simple.write_data())
    print("\n")


    args = ["ClassName", ["attribute1: string"], ["Method1(input):integer"],
            [("comp", "Class2"), ("extends", "Parent")]]


    mb = PythonClassBuilder(args[0])
    md = ClassDirector(mb)
    md.build_class(args)
    print(mb.new_class.write_data())

