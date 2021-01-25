""" Task 3: Add callback feature to urllib3.util.retry.Retry

Requirements:
    1. Create CallbackRetry class based on urllib3.util.retry.Retry
    2. Additional class arguments:
        a. callback: Callable. Optional, defaults to None
    3. If callback is None than work same way as Retry
       Otherwise call ``callback(o: RetryInfo)`` before increase retry counter
        a. RetryInfo is namedtuple with arguments:
            retry_status: RetryStatus object
            method: http method
            response: response object
        b. RetryStatus is namedtuple with arguments:
            total: Total retries
            connect: Total connect retries
            read: Total read retries
            redirect: Total redirects

Hints:
    1. For sending requests you can use httpbin.org (remote or local) endpoint /status/429
    2. For local httpbin.org you could use docker containers
        a. In terminal go to lesson_6 directory
        b. execute: docker-compose up
        c. server will available on http://127.0.0.1:8000
"""

