""" Task 1: Create function which return copy (!!!) of dictionary without selected keys

Requirement:
    1. Implement function del_dict_keys

    2. Functions arguments:
        a. ``d``: Dictionary to find
        b. ``*keys``: Keys in dictionary to delete

    3. Examples:
        >>> d = {'a': {'b': {'c': 1, 'd': 2}, 'e': 3}, 'f': 4, 'g': 5}
        >>> del_dict_keys(d, 'a', 'f')
        {'g': 5}
        >>> del_dict_keys(d, 'x', 'y', 'z')
        {'a': {'b': {'c': 1, 'd': 2}, 'e': 3}, 'f': 4, 'g': 5}
        >>> del_dict_keys(d, 'a', 'f', 'g')
        {}
"""
