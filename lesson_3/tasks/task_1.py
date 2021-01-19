""" Task 1: Create extended version of itertools.count() object

Requirement:
    1. Implement class Count based on Iterator

    2. Class arguments:
      a. ``name``: Name of count object. Optional. Default to None. String
      b: Start ``count`` value. Optional. Default to 0. Integer or float
      c: Count ``step``. Optional. Default to 1.

    3. Mandatory methods:
      a. implement __next__ method which return next counter value

    4. Create read-only properties
      a. name: counter name
      a. curval: counter current value
      b. nextval: counter next value (also it run __next__() method)

    5. Use Type Hinting + Docstring
"""

from collections.abc import Iterator


class Count(Iterator):
    """ Extend itertools.count() object """

    def __init__(self, name: str = None, start: int = 0, step: int = 1):
        """ Initialize object of Count

        Args:
            name: Name of count object. Optional. Default to None. String
            start: ``count`` value. Optional. Default to 0. Integer or float
            step: Optional. Default to 1.
        """
        self._name = name
        self._start = start
        self._step = step

    @property
    def name(self) -> str:
        """

        Returns:
            str: name of count object

        """
        return self._name

    @property
    def curval(self) -> int:
        """

        Returns:
            int: current value

        """
        return self._start

    @property
    def nextval(self) -> int:
        """

        Returns:
            int: next value

        """
        return self._start + self._step

    def __next__(self):
        self.buff = self._start
        self._start = self.nextval
        return self.buff


if __name__ == "__main__":
    print(help(Count))
    print()

    counter1 = Count(start=0, step=1)
    print("Counter: %r" % counter1.name)

    for _ in range(10):
        print(next(counter1))

    counter2 = Count(name="Awesome counter", start=2.5, step=0.5)
    print("Counter: %r" % counter2.name)

    for _ in range(10):
        print(next(counter2))
