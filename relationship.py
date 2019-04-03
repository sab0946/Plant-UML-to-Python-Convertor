class Relationship:

    """Builds the class relationship data
    >>> a = Relationship(('extends', 'Class2'))
    >>> print(a.name)
    Class2
    >>> print(a.type)
    extends
    >>> a = Relationship(('comp', 'Class3'))
    >>> print(a.name)
    Class3
    >>> print(a.type)
    comp
    """

    def __init__(self, new_type):
        self.name = new_type[1].lower()
        self.type = new_type[0]

    def __str__(self):
        return f"{self.name}s"


if __name__ == "__main__":
    from doctest import testmod
    testmod()
