""" Task 2: Create function decorator

Requirement:
    1. Implement function decorator simple_logger

    2. Before execute actual function decorator should output
        a. Function name
        b. all positional and keyword arguments with default values and their names

            inspect.getfullargspec
            https://docs.python.org/3/library/inspect.html#inspect.getfullargspec

            inspect.signature
            https://docs.python.org/3/library/inspect.html#inspect.signature

    3. After execute actual function should output
        a. time to execute in seconds.
            Number of execution should contain max 3 digits after point
                0.001 sec
                3.1 sec
                100500.0 sec
        b. Value which function return

    4. You should use print rather than logging module. But if you really want you can use logging

    5. Use Type Hinting + Docstring

    6. Decorated function should their own docstring
"""


def simple_logger(func):
    def wrapper():
        pass
    pass


if __name__ == "__main__":
    import time

    @simple_logger
    def simple_function(a):
        print(a)
        print("I'm return nothing!")

    @simple_logger
    def not_simple_function(sleep_time=3, result=42):
        print("I want to sleep")
        time.sleep(sleep_time)
        return result

    print(help(simple_function))
    simple_function("So Simple")

    print(help(simple_function))
    not_simple_function()

    not_simple_function(sleep_time=.1, result=100**100)
