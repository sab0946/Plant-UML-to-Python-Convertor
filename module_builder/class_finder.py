from .relationship_finder import RelationshipFinder

class ClassFinder:

    class_list = []

    @classmethod
    def find_classes(cls, class_content_list, relationship_content):
        for class_info in class_content_list:
            class_name = class_info.split(' ')[1]
            attributes = []
            methods = []
            relationships = []
            for line in class_info.split("\n"):
                if line.find(":") != -1 and line.find("(") == -1:
                    attributes.append(line)
            for line in class_info.split("\n"):
                if line.find("(") != -1:
                    methods.append(line)
            for relationship in relationship_content.split("\n"):
                if RelationshipFinder.find_relationship(relationship, class_name):
                    relationships.append(
                        RelationshipFinder.find_relationship(relationship, class_name))
            new_tuple = (class_name, attributes, methods, relationships)
            cls.class_list.append(new_tuple)
        return cls.class_list

