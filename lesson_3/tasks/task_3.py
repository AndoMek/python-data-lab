import re
from decimal import Decimal as decimal

""" Task 3: Create functions which convert from ``str`` to another Python Type

Requirement:
    1. Implement functions
        a. cast_to_bool: convert string to boolean
        b. cast_to_int: convert string value to integer
        c. cast_to_float: convert string to float
        d. cast_to_number: convert string to decimal.Decimal

    2. Functions arguments:
        a. value: String value

    3. Additional convert:
        a. should ignore any whitespaces in value.
        Note: Some types already ignore it

    3. Raise exceptions:
        a. TypeError: if function argument value not string
        b. ValueError: if failed to convert to selected type

    4. Use Type Hinting + Docstring

    5. Function should return own docstring
"""


def cast_to_bool(value: str):
    """ Convert string value to boolean

    Args:
        value: value to convert. String

    Returns:
        bool: True if successful, False otherwise.

    Raises:
        TypeError: If 'value' is not str.
        ValueError: If `value` is not equal to `bool` after transformation.
    """
    if not isinstance(value, str):
        raise TypeError
    boolean = re.findall('[A-Za-z]{4,5}', value)
    if boolean:
        boolean = boolean[0].lower()
    else:
        raise ValueError
    if boolean == 'true':
        return True
    elif boolean == 'false':
        return False
    else:
        raise ValueError


print(cast_to_bool.__doc__)
try:
    print(cast_to_bool("true"))
    print(cast_to_bool("TruE"))
    print(cast_to_bool("fALse"))
    print(cast_to_bool(" fALse\t"))
    print(cast_to_bool("Yes"))
except ValueError as v_error:
    print(v_error)
    print("Value error at cast_to_bool\n")
except TypeError as t_error:
    print(t_error)
    print("TypeError at cast_to_bool\n")


def cast_to_int(value: str):
    """ Convert string value to integer

    Args:
        value: value to convert. String

    Returns:
        int: value

    Raises:
        TypeError: If 'value' is not str.
        ValueError: If `value` is not equal to `int` after transformation.
    """
    if not isinstance(value, str):
        raise TypeError
    int_value = re.findall('[-]?[0-9]+', value)
    if int_value:
        int_value = int(int_value[0])
    else:
        raise ValueError
    if isinstance(int_value, int):
        return int_value
    else:
        raise ValueError


print(cast_to_int.__doc__)
try:
    print(cast_to_int("1"))
    print(cast_to_int("1234567890987654321"))
    print(cast_to_int(" -1\t"))
    print(cast_to_int("one"))
except ValueError as v_error:
    print(v_error)
    print("Value error at cast_to_int\n")
except TypeError as t_error:
    print(t_error)
    print("TypeError at cast_to_int\n")


def cast_to_float(value: str):
    """ Convert string value to float

    Args:
        value: value to convert. String

    Returns:
        float: value

    Raises:
        TypeError: If 'value' is not str.
        ValueError: If `value` is not equal to `float` after transformation.
    """
    if not isinstance(value, str):
        raise TypeError
    float_value = re.findall('[-]?([0-9]*.[0-9]+|[0-9]+)', value)
    if float_value:
        float_value = float(float_value[0])
    else:
        raise ValueError
    if isinstance(float_value, float):
        return float_value
    else:
        raise ValueError


print(cast_to_float.__doc__)
try:
    print(cast_to_float("1"))
    print(cast_to_float("123456789.0987654321"))  # output 123456789.09876543
    print(cast_to_float(" -111.111\t"))
    print(cast_to_float("PI"))
except ValueError as v_error:
    print(v_error)
    print("Value error at cast_to_float\n")
except TypeError as terror:
    print(t_error)
    print("TypeError at cast_to_float\n")


def cast_to_number(value: str):
    """ Convert string value to decimal.Decimal

    Args:
        value: value to convert. String

    Returns:
        decimal.Decimal: value

    Raises:
        TypeError: If 'value' is not str.
        ValueError: If `value` is not equal to `decimal.Decimal` after transformation.
    """
    if not isinstance(value, str):
        raise TypeError
    dec_value = re.findall('[-]?([0-9]*.[0-9]+|[0-9]+)', value)
    if dec_value:
        dec_value = decimal(dec_value[0])
    else:
        raise ValueError
    if isinstance(dec_value, decimal):
        return dec_value
    else:
        raise ValueError


print(cast_to_number.__doc__)
try:
    print(cast_to_number("1"))
    print(cast_to_number("123456789.0987654321"))
    print(cast_to_number(" -111.111\t"))
    print(cast_to_number("PI"))
except ValueError as v_error:
    print(v_error)
    print("Value error at cast_to_number\n")
except TypeError as t_error:
    print(t_error)
    print("TypeError at cast_to_number\n")
