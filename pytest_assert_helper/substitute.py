import re


class Substitute:
    """Substitutes act as proxies for other objects for use with asserts.

    A Substitute should be used whenever the exact expected value of an object
    is uncertain, but you still have some expectations for what it will be.
    Once a Substitute has been successfully compared to another object, it will
    remember that object and use it in future comparisons. For example:
    ```
    x = Any() # a generic substitute
    assert x == 1 # x will now "remember" the value 1
    assert x != 2 # 1 != 2
    ```
    It is not possible to apply functions or operations to a Substitute during
    an assert statement:
    ```
    x = Any()
    assert (x, x**2) == (3, 9) # TypeError: __pow__ is not defined for type Any
    ```
    """

    _matched = False
    _match = None

    def _eq(self, other):
        raise NotImplementedError

    def _str(self):
        raise NotImplementedError

    def _repr(self):
        raise NotImplementedError

    def __eq__(self, other):
        if self._matched:
            return self._match == other
        try:
            if self._eq(other):
                self._matched = True
                self._match = other
                return True
        except Exception:
            pass
        return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        if self._matched:
            return hash(self._match)
        return hash(super())

    def __str__(self):
        if self._matched:
            return str(self._match)
        try:
            return self._str()
        except NotImplementedError:
            return repr(super())

    def __repr__(self):
        if self._matched:
            return repr(self._match)
        try:
            return self._repr()
        except NotImplementedError:
            return repr(super())


class Any(Substitute):
    """Matches any object, including None."""

    def _eq(self, other):
        return True

    def _str(self):
        return "Any()"

    def _repr(self):
        return "Any()"


class Type(Substitute):
    """Matches any object with the given type."""

    def __init__(self, clazz):
        self.clazz = clazz

    def _eq(self, other):
        return isinstance(other, self.clazz)

    def _str(self):
        return "Type(%s)" % str(self.clazz)

    def _repr(self):
        return "Type(%s)" % repr(self.clazz)


class Re(Substitute):
    """Matches any string that fully matches the given regular expression."""

    def __init__(self, pattern):
        if isinstance(pattern, type(re.compile(""))):
            self.pattern = pattern
        else:
            self.pattern = re.compile(pattern)

    def _eq(self, other):
        return self.pattern.fullmatch(other) is not None

    def _str(self):
        return self.pattern.pattern

    def _repr(self):
        return repr(self.pattern.pattern)


# Some dandi specific things


class Id(Re):
    """Matches a 24 character hexadecimal ID."""

    def __init__(self):
        super().__init__("[0-9a-f]{24}")


class Timestamp(Re):
    """Matches a reasonably well-formed timestamp."""

    # TODO: consider using datetime instead of a regex
    def __init__(self):
        super().__init__(r"\d{4}-\d{2}-\d{2}T\d{2}\:\d{2}\:\d{2}\.\d{6}\+\d{2}\:\d{2}",)
