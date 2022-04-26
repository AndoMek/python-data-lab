import time


def main():
    start = time.time()
    print("Start import function_2 from sample_module_2")
    from sample_module_2 import function_2
    print("Complete import function_2 from sample_module_2 after %.3fms" %
          ((time.time() - start) * 1000))

    function_2()

    start = time.time()
    print("Start import function_1 from sample_module_1")
    from sample_module_1 import function_1
    print("Complete import function_1 from sample_module_1 after %.3fms" %
          ((time.time() - start) * 1000))

    function_1()

    print()

if __name__ == "__main__":
    main()
