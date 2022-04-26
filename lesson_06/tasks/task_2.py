import requests
from requests.auth import AuthBase
import json
from task_1 import err, out
import logging

""" Task 2: 


Requirements:
    1. This class should take two mandatory arguments:
        a. key_id: string
        b. secret_key: string
    2. If http method one of: POST, PUT, PATCH than add to json data additional keys:
        {'key_id': key_id, 'secret_key': secret_key}
       Otherwise raise some exception with text that this method not allowed

Hints:
    1. For sending requests you can use httpbin.org (remote or local) endpoint /anything
    2. For local httpbin.org you could use docker containers
        a. In terminal go to lesson_6 directory
        b. execute: docker-compose up
        c. server will available on http://127.0.0.1:8000
"""
logger = logging.getLogger(__name__)
logger.addHandler(out())
logger.addHandler(err())
logger.setLevel(logging.DEBUG)


class HttpMethod(ValueError):
    pass


class SimpleAuth(AuthBase):
    def __init__(self, key_id: str, secret_key: str):
        self._key_id = key_id
        self._secret_key = secret_key

    def __call__(self, r):
        methods = frozenset(['POST', 'PUT', 'PATCH'])
        if r.method not in methods:
            logger.error(f"Http method one of: POST, PUT, PATCH. Method are {r.method}")
            raise HttpMethod(f"Http method one of: POST, PUT, PATCH. Method are {r.method}")
        key = {
            'key_id': self._key_id,
            'secret_key': self._secret_key
        }
        body = r.body
        dictionary = body.decode("UTF-8")
        dictionary = json.loads(dictionary)
        dictionary = {**dictionary, **key}
        r.body = json.dumps(dictionary)
        return r


if __name__ == "__main__":
    valve = {"International": "2021", "Winner": "Na'Vi"}
    with requests.Session() as session:
        res = session.post('http://127.0.0.1:8000/post', auth=SimpleAuth('na', 'vi'), json=valve)
        print(res.json())
        print(res.raise_for_status())
        print(res.status_code)

