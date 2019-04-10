import re


def find_type(new_type):
    type_list = ["string", "number", "list", "tuple", "dict"]
    type_dict = {"string": "str", "number": "int",
                 "list": "list", "tuple": "tuple",
                 "dict": "dict"}
    if new_type in type_list:
        return type_dict.get(type_list[type_list.index(new_type)], "")
