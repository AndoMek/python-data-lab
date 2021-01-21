from typing import Dict, Union

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


def get_dict_value(dictionary: Dict, *keys: str, default: int = None, errors: str = 'ignore') -> Union[int, None]:
    """ Find keys from dictionary and return value
    Args:
        dictionary: dictionary to find
        *keys: Variable length argument list.
        default: value to return if key doesnt exists
        errors: key-word. Default 'ignore'. 'strict' to raise error if key doesnt exists
    Returns:
        value
    """
    try:
        if isinstance(dictionary[keys[0]], dict):
            return get_dict_value(dictionary[keys[0]], *keys[1:], default=default, errors=errors)
        else:
            if len(keys) == 1:
                return dictionary[keys[0]]
            else:
                raise KeyError

    except KeyError:
        if errors == 'strict':
            raise KeyError('.'.join(keys))
        elif default:
            return default
        else:
            return None


if __name__ == "__main__":
    d = {'a': {'b': {'c': 1, 'd': 2}, 'e': 3}, 'f': 4}
    print(get_dict_value(d, 'a', 'b', 'd'))
    print(get_dict_value(d, 'xxx'))
    print(get_dict_value(d, 'a', 'b', 'z'))
    print(get_dict_value(d, 'a', 'b', 'z', default=42))
    print(get_dict_value(d, 'a', 'b', 'z', default=42, errors='strict'))
