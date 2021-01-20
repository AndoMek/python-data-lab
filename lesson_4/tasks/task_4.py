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
