from typing import Dict
import copy

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


def find_key(d: Dict, key: str):
    try:
        message = d.pop(key, None)
        if not message:
            raise KeyError
    except KeyError:
        for value in d.values():
            if isinstance(value, dict):
                find_key(value, key)


def del_dict_keys(dictionary: Dict, *keys: str) -> Dict:
    """ Delete keys from dictionary
    Function print:
        dictionary after transformation
    Args:
        dictionary: dictionary to remove keys
        *keys: Variable length argument list.
    Returns:
        dictionary without selected keys
    """
    new_d = copy.deepcopy(dictionary)
    for key in keys:
        find_key(new_d, key)
    return new_d


if __name__ == "__main__":
    d = {'a': {'b': {'c': 1, 'd': {'h': 4}}, 'e': 3}, 'f': {'c': 1, 'd': 2}, 'g': {'l': {'h': 5}, 'k': 5}}
    print(del_dict_keys(d, 'a', 'f'))
    print(del_dict_keys(d, 'x', 'y', 'z'))
    print(del_dict_keys(d, 'a', 'f', 'g'))
    print(del_dict_keys(d, 'c', 'd'))
    print(del_dict_keys(d, 'h'))
    print(del_dict_keys(d, 'h', 'l', 'd'))
