from collections.abc import Mapping
""" Task 4: Create class ExtendedMapping which allow to call mapping key as attribute

Requirement:
    1. Implement class ExtendedMapping based on collections.abc.Mapping
        a. Class arguments:
            i. ``m``: Original Mapping object. Positional only

    2. Raises
        TypeError: If ``m`` argument not Mapping
        ValueError: If key not valid Python identifier or key not string
        KeyError: If key not exists
        AttributeError: If attribute not exists

    3. Examples:
        >>> d1 = {'a': {'b': {'c': 1, 'd': 2}, 'e': 3}, 'f': 4}
        >>> em1 = ExtendedMapping(d)
        >>> em1["a"]
        {'b': {'c': 1, 'd': 2}
        >>> em1.a
        {'b': {'c': 1, 'd': 2}
        >>> em1.f
        4
        >>> em1.z
        Traceback (most recent call last):
        ...
        AttributeError: 'ExtendedMapping' object has no attribute 'z'
        >>> em1["x"]
        Traceback (most recent call last):
        ...
        KeyError: 'x'
        >>> d2 = {'2key': {'b': {'c': 1, 'd': 2}, 'e': 3}, 'a': 4}
        >>> em2 = ExtendedMapping(d2)
        Traceback (most recent call last):
        ...
        ValueError: '2key' not valid Python identifier
"""


class ExtendedMapping(Mapping):
    def __init__(self, m):
        self.check_values(m)
        self.m = m
        if not isinstance(m, Mapping):
            raise TypeError

    def check_values(self, d: dict):
        is_int = False
        for key, value in d.items():
            if isinstance(key, str):
                try:
                    int(key[0])
                    is_int = True
                except ValueError:
                    pass
                if is_int:
                    raise ValueError(f"'{key}' not valid Python identifier")
            else:
                raise ValueError(f"'{key}' not valid Python identifier")
            if isinstance(value, dict):
                self.check_values(value)

    def __len__(self) -> int:
        return len(self.m)

    def __iter__(self) -> Mapping:
        yield from self.m

    def __getitem__(self, key: str) -> int:
        if isinstance(key, str):
            try:
                return self.m[key]
            except KeyError:
                raise KeyError(f"'ExtendedMapping' object has no key: '{key}'")
        else:
            raise ValueError

    def __getattr__(self, item: str) -> int:
        if isinstance(item, str):
            try:
                return self.m[item]
            except KeyError:
                raise AttributeError(f"'ExtendedMapping' object has no attribute: '{item}'")
        else:
            raise ValueError


if __name__ == '__main__':
    d1 = {'a': {'b': {'c': 1, 'd': 2}, 'e': 3}, 'f': 4}
    em1 = ExtendedMapping(d1)
    print(em1['a'])
    print(em1.a)
    # print(em1['a1'])
    # print(em1.a1)
    # d2 = {'2key': {'b': {'c': 1, 'd': 2}, 'e': 3}, 'a': 4}
    # em2 = ExtendedMapping(d2)
    d2 = {'d': {'b': {'c': 1, 2: 2}, 'e': 3}, 'a': 4}
    em2 = ExtendedMapping(d2)

