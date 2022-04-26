import time


def function_2():
    time.sleep(2)
    print("Function 2: %r. Path: %r" % (__name__, __file__))


if __name__ == "__main__":

    time.sleep(2)
    function_2()
