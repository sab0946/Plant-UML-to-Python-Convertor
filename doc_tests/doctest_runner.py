# Runs all individual doctest files


def test():
    import doctest
    doctest.testfile('attribute_doctest', verbose=1)
    doctest.testfile('class_builder_doctest', verbose=1)
    doctest.testfile('interpreter_doctest', verbose=1)
    doctest.testfile('method_doctest', verbose=1)
    doctest.testfile('module_doctest', verbose=1)
    doctest.testfile('relationship_doctest', verbose=1)


if __name__ == "__main__":
    test()
