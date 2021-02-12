import os
import platform
from functools import partial


def default(v, d="unknown"):
    return v or d


def main():
    pr = partial(print, sep=": ")

    pr("\nSystem")
    pr("System Name", default(platform.system()))
    pr("System Release", default(platform.release()))
    pr("Processor", default(platform.processor()))
    pr("Machine type", default(platform.machine()))
    pr("Network name", default(platform.node()))

    pr("\nPython")
    pr("Version", default(platform.python_version()))
    pr("Implementation", default(platform.python_implementation()))
    pr("Build", default(platform.python_build()))
    pr("Compiler", default(platform.python_compiler()))

    pr("\nEnvironmnent Variables")
    for k, v in os.environ.items():
        pr(k, v)


if __name__ == '__main__':
    main()
