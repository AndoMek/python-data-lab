from abc import ABCMeta, abstractmethod
import re
from decimal import Decimal as decimal
from decimal import InvalidOperation
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


class BaseCastType(metaclass=ABCMeta):
    @abstractmethod
    def __call__(self, values):
        pass

    @staticmethod
    def check_input_value(value: str):
        """Check value

        Args:
            value: checked value
        Returns:
            value if string
        """
        if isinstance(value, str):
            return value
        else:
            raise TypeError(f"TypeError  with value {value}")


class BoolCastType(BaseCastType):
    """Cast to Bool"""

    def __call__(self, values):
        self.values = BaseCastType.check_input_value(values)
        boolean = re.findall('[A-Za-z]{4,5}', self.values)
        if boolean:
            boolean = boolean[0].lower()
        else:
            raise ValueError(f"ValueError with {self.values}")
        if boolean == 'true':
            return True
        elif boolean == 'false':
            return False
        else:
            raise ValueError(f"ValueError with {self.values}")


class IntCastType(BaseCastType):
    """Cat to Integer"""

    def __call__(self, values):
        integer_v = BaseCastType.check_input_value(values)
        try:
            return int(integer_v.strip())
        except ValueError:
            raise ValueError(f"ValueError with {integer_v}")


class FloatCastType(BaseCastType):
    """Cast to Float"""
    def __call__(self, values):
        float_v = BaseCastType.check_input_value(values)
        try:
            return float(float_v.strip())
        except ValueError:
            raise ValueError(f"ValueError with {float_v }")


class NumberCastType(BaseCastType):
    """Cast to Decimal"""
    def __call__(self, values):
        dec = BaseCastType.check_input_value(values)
        try:
            return decimal(dec.strip())
        except ValueError:
            raise ValueError(f"ValueError with {dec}")
        except InvalidOperation:
            raise ValueError(f"ValueError with {dec}")


if __name__ == '__main__':
    boolean = BoolCastType()
    try:
        print(boolean("true"))
        print(boolean("TruE"))
        print(boolean("fALse"))
        print(boolean(" fALse\t"))
        print(boolean("Yes"))
    except ValueError as v_error:
        print(v_error)
    except TypeError as t_error:
        print(t_error)

    integer = IntCastType()
    try:
        print(integer("1"))
        print(integer("1234567890987654321"))
        print(integer(" -1\t"))
        print(integer("one"))
    except ValueError as v_error:
        print(v_error)
    except TypeError as t_error:
        print(t_error)

    float_v = FloatCastType()
    try:
        print(float_v("1"))
        print(float_v("123456789.0987654321"))  # output 123456789.09876543
        print(float_v(" -111.111\t"))
        print(float_v("PI"))
    except ValueError as v_error:
        print(v_error)
    except TypeError as t_error:
        print(t_error)

    dec = NumberCastType()
    try:
        print(dec("1"))
        print(dec("123456789.0987654321"))
        print(dec(" -111.111\t"))
        print(dec("PI"))
    except ValueError as v_error:
        print(v_error)
    except TypeError as t_error:
        print(t_error)
