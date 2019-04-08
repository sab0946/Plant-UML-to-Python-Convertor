from module_builder.class_builder import ClassBuilder


class ClassAdder:

    @classmethod
    def add_class(cls, class_name, attributes, methods, relationships):
        new_class = ClassBuilder()
        new_class.build_class(class_name, attributes, methods, relationships)
        return new_class
