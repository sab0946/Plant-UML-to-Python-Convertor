import re
from .class_builder import ClassBuilder
from .module import Module
from .shelver import Shelver
from .db_writer import DbWriter
from .class_finder import ClassFinder


class Interpreter:

    def __init__(self):
        self.my_file = ""
        self.my_shelf = None
        self.my_class_content = []
        self.my_relationship_content = ""
        self.all_my_classbuilders = []
        self.all_my_modules = []
        self.all_my_errors = []
        self.my_db = None

    def add_class(self, class_name, attributes, methods, relationships):
        new_class = ClassBuilder()
        new_class.build_class(class_name, attributes, methods, relationships)
        self.all_my_classbuilders.append(new_class)

    def add_module(self, new_module_name, new_classes):
        new_module = Module()
        new_module.create_module(new_module_name, new_classes)
        self.all_my_modules.append(new_module)


class FileReader (Interpreter):

    def __init__(self):
        Interpreter.__init__(self)

    def add_file(self, file_name, new_module_name):
        self.my_file = file_name
        self.read_file()
        my_classes = ClassFinder.find_classes(self.my_class_content, self.my_relationship_content)
        for a_class in my_classes:
            self.add_class(a_class[0], a_class[1], a_class[2], a_class[3])
        self.add_module(new_module_name, self.all_my_classbuilders)

    def read_file(self):
        try:
            with open(self.my_file, "rt") as my_file:
                contents = my_file.read()
                class_results = re.split(r"}", contents)
                self.my_relationship_content = \
                    class_results[len(class_results) - 1]
                class_results.remove(class_results[len(class_results) - 1])
                for result in class_results:
                    self.my_class_content.append(result)
        except FileNotFoundError as e:
            self.all_my_errors.append(e)
            print("Error - File not found")


class ModuleWriter(Interpreter):

    def __init__(self):
        Interpreter.__init__(self)

    def write_modules(self):
        for a_module in self.all_my_modules:
            root_name = a_module.write_files()[0]
            folder_content = a_module.write_files()[1]
            for a_folder in folder_content:
                try:
                    file_name = f"{root_name}/{a_folder[0]}"
                    with open(file_name, "w+") as f:
                        f.write(a_folder[1])
                except FileNotFoundError as e:
                    self.all_my_errors.append(e)
                    print("Error - Directory does not exist")


class UmlInterpreter(FileReader, ModuleWriter):

    language = "Plant UML"

    def __init__(self):
        FileReader.__init__(self)
        ModuleWriter.__init__(self)

    def interpret(self, source_file, write_folder):
        self.add_file(source_file, write_folder)
        self.write_modules()


class ModuleShelver (UmlInterpreter):
    """shelves the module data to a file"""

    def __init__(self):
        UmlInterpreter.__init__(self)

    def shelve_modules(self, shelf_file):
        shelf = Shelver(shelf_file)
        for a_module in self.all_my_modules:
            shelf.shelve_modules(a_module)
        self.my_shelf = shelf.my_shelf_file


class DbCreator (UmlInterpreter):
    """creates a database writer class"""

    def __init__(self):
        UmlInterpreter.__init__(self)

    def create_db(self):
        db = DbWriter()
        for a_module in self.all_my_modules:
            db.write_db(a_module)
        self.my_db = db
