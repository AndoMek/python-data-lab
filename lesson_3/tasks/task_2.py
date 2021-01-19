import inspect

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
    def wrapper(*args, **kwargs):
        """ Logging decorator
        Function print:
            Before execute original function:
                Function name
                Argument description
                Argument signature
            After execute:
                Execution time
                Return Value (if exists)

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        start = time.time()
        print(f"Function name: {func.__name__}")
        print(f"Argument description:\n{inspect.getfullargspec(func)}\n")
        print(f"Signature:\n {inspect.signature(func)}\n")
        result = func(*args, **kwargs)
        print("\nExecution time:\t%.3f\n\n" % (time.time() - start))
        if result is not None:
            print(f"\nResult:\t{result}\n")

    return wrapper


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

    not_simple_function(sleep_time=.1, result=100 ** 100)
