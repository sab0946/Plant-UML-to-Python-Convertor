class Relationship:

    """Builds the class relationship data"""

    def __init__(self, new_type, my_class_builder=None):
        self.my_class_builder = my_class_builder
        self.name = new_type[1].lower() + "s"
        self.type = new_type[0]
        self.method_name = "add_" + str(self.type)

    def __str__(self):
        return f"{self.name}s"

    def return_type(self):
        return self.type

    def add_comp(self):
        self.my_class_builder.all_my_composite_classes.append(self.name)

    def add_assos(self):
        self.my_class_builder.all_my_associated_classes.append(self.name)

    def add_extends(self):
        self.my_class_builder.all_my_parent_classes.append(self.name)

    def add_relationship(self):
        method = getattr(self, self.method_name)
        return method()
