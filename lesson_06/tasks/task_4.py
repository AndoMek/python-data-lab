from lesson_6.tasks.task_3 import CallbackRetry, callback
from requests.adapters import HTTPAdapter
import requests
from typing import Callable

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


def session_fun(retries: int = 5, session: requests.Session = None,
                status_forcelist: frozenset = frozenset([429, 500, 502, 504]),
                backoff_factor: float = 0.3, method_whitelist: str = ['GET', 'HEAD'],
                pool_connections: int = requests.adapters.DEFAULT_POOLSIZE,
                pool_maxsize: int = requests.adapters.DEFAULT_POOLSIZE,
                pool_block: int = requests.adapters.DEFAULT_POOLBLOCK,
                callback: Callable = None) -> requests.Session:
    """Custom requests.Session

    Args:
        retries: variable set to total, read, connect. Optional, default to 5
        session: request.Session to extend. Optional, default None
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
        callback: Callable. Optional, defaults to None

    Returns:
        requests.Session with configured retries
    """
    ret = CallbackRetry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        method_whitelist=method_whitelist,
        callback=callback
    )
    s = session or requests.Session()
    adapter = HTTPAdapter(max_retries=ret, pool_maxsize=pool_maxsize, pool_block=pool_block,
                          pool_connections=pool_connections)
    s.mount('http://', adapter)
    s.mount('https://', adapter)

    return s


if __name__ == "__main__":
    with requests.Session() as session:
        session = session_fun(session=session, callback=callback)
        res = session.get("http://127.0.0.1:8000/status/429")
