def function_1():
    print("Function 1: %r. Path: %r" % (__name__, __file__))


if __name__ == "__main__":
    import time
    time.sleep(2)

    function_1()
