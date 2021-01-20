""" Task 2: Create function which find and return values into dict / nested dict

Requirement:
    1. Implement function get_dict_value

    2. Functions arguments:
        a. ``d``: Dictionary to find
        b. ``*keys``: Keys in dictionary to find value
        c. ``default``: Default value if keys path not exists. Default ot `None`
        d. ``errors``: Behavior if keys path not exists:
            if set 'ignore' than return ``default_value``
            if set 'strict' - than raise KeyError
            Default to 'ignore'

    3. Examples:
        >>> d = {'a': {'b': {'c': 1, 'd': 2}, 'e': 3}, 'f': 4}
        >>> get_dict_value(d, 'a', 'b', 'd')
        2
        >>> get_dict_value(d, 'xxx')
        None
        >>> get_dict_value(d, 'a', 'b', 'z')
        None
        >>> get_dict_value(d, 'a', 'b', 'z', default=42)
        42
        >>> get_dict_value(d, 'a', 'b', 'z', default=42, errors='strict')
        Traceback (most recent call last):
        ...
        KeyError: Key path 'a.b.z' not exists

"""
