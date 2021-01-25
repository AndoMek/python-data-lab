""" Task 4: Create function which return requests.Session instance class with configured retries

Requirements:
    1. Create function with arguments:
        retries: Number of retries.
            Optional, default to 5
        session: request.Session to extend.
            If not set than create new request.Session()
        status_forcelist: A set of integer HTTP status codes that we should force a retry on.
            Optional, default to frozenset([429, 500, 502, 504])
        backoff_factor: A backoff factor to apply between attempts after the second try.
            Optional, default: 0.3
        method_whitelist: Whitelist methods for retry.
            Optional, if not set than GET and HEAD methods
        pool_connections: The number of urllib3 connection pools to cache.
            Optional, if not set than use requests.adapters.DEFAULT_POOLSIZE
        pool_maxsize: The maximum number of connections to save in the pool.
            Optional, if not set than use requests.adapters.DEFAULT_POOLSIZE
        pool_block: Whether the connection pool should block for connections.
            Optional: if not set than use requests.adapters.DEFAULT_POOLBLOCK
    2. Function should return Request Session object with configured HTPPAdapter which initialised with:
        a. urllib3.util.retry.Retry object (`retries` variable set to total, read, connect)
        b. pool_connections, pool_maxsize, pool_block
        c. Uses for all http and https connections

Nice to Have:
    1. Instead of urllib3.util.retry.Retry use CallbackRetry from lesson_6.task_3
    2. Add to function additional arguments:
        callback: Callback callable object
            Optional, default to None

Hints:
    1. For sending requests you can use httpbin.org (remote or local) endpoint /status/429
    2. For local httpbin.org you could use docker containers
        a. In terminal go to lesson_6 directory
        b. execute: docker-compose up
        c. server will available on http://127.0.0.1:8000
"""
