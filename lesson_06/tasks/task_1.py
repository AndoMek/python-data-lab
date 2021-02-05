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
