import re


class RelationshipFinder:

    @classmethod
    def find_relationship(cls, relationship, class_name):
        if relationship.startswith(class_name):
            if len(relationship.split(" ")) < 2:
                pass
            if re.search(r"\*--", relationship):
                com_class = relationship.split(" ")[4]
                return tuple(("comp", com_class))
            if re.search(r"--", relationship):
                as_class = relationship.split(" ")[4]
                return tuple(("assos", as_class))
        elif relationship.endswith(class_name):
            if len(relationship.split(" ")) < 2:
                pass
            if re.search(r"<\|--", relationship):
                ext_class = relationship.split(" ")[0]
                return tuple(("extends", ext_class))
