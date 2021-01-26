import logging
from urllib3.util.retry import Retry
from task_1 import out, err
from collections import namedtuple
from requests.adapters import HTTPAdapter
import requests

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
logger = logging.getLogger(__name__)
logger.addHandler(out())
logger.addHandler(err())
logger.setLevel(logging.DEBUG)
RetryInfo = namedtuple(
    "RetryInfo",
    ["retry_status", "method", "response"])
RetryStatus = namedtuple(
    "RetryStatus",
    ["total", "connect", "read", "redirect"])


class CallbackRetry(Retry):
    """Make custom Retry
    """
    def __init__(self, *args, **kwargs):
        self._callback = kwargs.pop('callback', None)
        logger.info(f'This is an info message, callback is {self._callback}')
        super(CallbackRetry, self).__init__(*args, **kwargs)

    def new(self, **kwargs):
        kwargs['callback'] = self._callback
        return super(CallbackRetry, self).new(**kwargs)

    def increment(self, method, url, response, *args, **kwargs):
        if self._callback:
            try:
                self._callback(
                    RetryInfo(RetryStatus(self.total, self.connect, self.read, self.redirect), method, response))
            except Exception as exp:
                logger.error(f'This is an error message, callback is failed {exp}')
        return super(CallbackRetry, self).increment(method, url, response, *args, **kwargs)


def callback(o: RetryInfo):
    print(o)


if __name__ == "__main__":
    with requests.Session() as session:
        retries = CallbackRetry(
            total=5,
            read=5,
            connect=5,
            backoff_factor=0.2,
            status_forcelist=[429, 502, 503, 504, ],
            callback=callback
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        res = session.get("http://127.0.0.1:8000/status/429")
