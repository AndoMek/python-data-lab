import logging
import sys

logger = logging.getLogger(__name__)
""" Task 1: Logging to stdout and stderr

Requirements:
    1. Create module logger
    2. Add two logging.StreamHandler for module logger
        a. First handler send to sys.stdout all messages with severity less or equal logging.INFO
        b. Second handler send to sys.stderr all messages with severity greater than logging.INFO
        c. Handlers shouldn't initialize if module import internally
    3. You could check that it work properly by run in terminal
        a. Only stdout:
        python ./lesson_6/tasks/task_1.py 2>/dev/null

        b. Only stderr:
        python ./lesson_6/tasks/task_1.py 1>/dev/null
"""
formatter = logging.Formatter(
    fmt="%(asctime)s.%(msecs)06d|%(levelname)s|%(pathname)s:%(funcName)s:%(lineno)-2s|%(message)s",
    datefmt="%Y-%m-%d,%H:%M:%S",
)


class LowerThanFilter(logging.Filter):
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno < self.level


def out():
    ltw = LowerThanFilter(logging.WARNING)
    stream_handler_out = logging.StreamHandler(sys.stdout)
    stream_handler_out.addFilter(ltw)
    stream_handler_out.setFormatter(formatter)
    return stream_handler_out


def err():
    stream_handler_out = logging.StreamHandler(stream=sys.stderr)
    stream_handler_out.setLevel(logging.WARNING)
    stream_handler_out.setFormatter(formatter)
    return stream_handler_out


if __name__ == "__main__":
    logger.addHandler(out())
    logger.addHandler(err())
    logger.setLevel(logging.DEBUG)
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')
