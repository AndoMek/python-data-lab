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


def cast_to_bool(value):
    """ Convert string value to boolean

    Examples:
        >>> cast_to_bool("true")
        True
        >>> cast_to_bool("TruE")
        True
        >>> cast_to_bool("fALse")
        False
        >>> cast_to_bool(" fALse\t")
        False
        >>> cast_to_bool("Yes")
        Traceback (most recent call last):
        ...
        ValueError: Can't cast 'Yes' to Python bool
    """


def cast_to_int(value):
    """ Convert string value to integer

    Examples:
        >>> cast_to_int("1")
        1
        >>> cast_to_int("1234567890987654321")
        1234567890987654321
        >>> cast_to_int(" -1\t")
        -1
        >>> cast_to_int("one")
        Traceback (most recent call last):
        ...
        ValueError: Can't cast 'one' to Python int
    """


def cast_to_float(value):
    """ Convert string value to float

    Examples:
        >>> cast_to_float("1")
        1.0
        >>> cast_to_float("123456789.0987654321")
        123456789.09876543
        >>> cast_to_float(" -111.111\t")
        -111.111
        >>> cast_to_float("PI")
        Traceback (most recent call last):
        ...
        ValueError: Can't cast 'PI' to Python float
    """


def cast_to_number(value):
    """ Convert string value to decimal.Decimal

    Examples:
        >>> cast_to_number("1")
        Decimal('1')
        >>> cast_to_number("123456789.0987654321")
        Decimal('123456789.0987654321')
        >>> cast_to_number(" -111.111\t")
        Decimal('-111.111')
        >>> cast_to_number("PI")
        Traceback (most recent call last):
        ...
        ValueError: Can't cast 'PI' to Python decimal.Decimal
    """
