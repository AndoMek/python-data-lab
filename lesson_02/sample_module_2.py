import time


def function_2():
    print("Function 2: %r. Path: %r" % (__name__, __file__))


time.sleep(2)
function_2()
