""" Task 3: Create classes which convert from ``str`` to another Python Type

Requirement:
    1. Implement abstract class BaseCastType
        a. Class arguments:
            i. ``value``: String value to cast

        b. Abstract methods:
            i. __call__(self): Method which return converted value

    2. Implement class BoolCastType which inherit from BaseCastType and implement __call__(self) method
    3. Implement class IntCastType which inherit from BaseCastType and implement __call__(self) method
    4. Implement class FloatCastType which inherit from BaseCastType and implement __call__(self) method
    5. Implement class NumberCastType which inherit from BaseCastType and implement __call__(self) method

    6. See examples in Lesson 3 Task 3
        a: Ignore trailing and leading whitespaces before converted to selected type.
    7. Raises
        TypeError: If ``value`` argument not string
        ValueError: if failed to convert to selected type
"""
