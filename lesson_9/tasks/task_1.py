import requests
from typing import Callable
from io import BytesIO
import gzip


def zip_payload(payload: str) -> bytes:
    btsio = BytesIO()
    g = gzip.GzipFile(fileobj=btsio, mode='w')
    g.write(bytes(payload, 'utf8'))
    g.close()
    return btsio.getvalue()


def add_header_hook(r, *args, **kwargs):
    r.headers.update({
        'Content-Encoding': 'gzip'})

    return r


def raise_on_error(r, *args, **kwargs):
    r.raise_for_status()
    return


class PreRequestHooks():
    def __init__(self, *hooks, session=None):
        self._hooks = hooks
        self._session = session or requests.Session()
        self._closed = False

    @property
    def session(self):
        return self._session

    @property
    def closed(self):
        return self._closed

    @property
    def hooks(self):
        return self._hooks

    def __enter__(self):
        if self._closed:
            raise SystemError("%r object are closed" % self.__class__)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not self._closed:
            self.session.close()

    def request(self, method, url, headers=None, files=None,
                data=None, params=None, auth=None, cookies=None,
                hooks=None, json=None):

        request = requests.Request(
            method, url,
            headers=headers,
            files=files,
            data=data,
            params=params,
            auth=auth,
            cookies=cookies,
            hooks=hooks,
            json=json,
        )

        for hook in self._hooks:
            if not isinstance(hook, Callable):
                raise TypeError("Hook expected callable object but got %r" % hook.__class__)
            request = hook(request)

        prepared = request.prepare()
        return self._session.send(prepared)

    def get(self, url, **kwargs):
        return self.request('GET', url, **kwargs)

    def options(self, url, **kwargs):
        return self.request('OPTIONS', url, **kwargs)

    def head(self, url, **kwargs):
        return self.request('HEAD', url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.request('POST', url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.request('PUT', url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self.request('PATCH', url, data=data, **kwargs)


def delete(self, url, **kwargs):
    return self.request('DELETE', url, **kwargs)


def sent_message(session: requests.Session, url, message: str = "Lorem ipsum dolor"):
    s = session or requests.Session()
    if s.headers.get('Content-Encoding') == 'gzip':
        pre_requests = PreRequestHooks(session=s)
        resp_hooks = pre_requests.post(url)
        print(resp_hooks.text)
    else:
        zipped_payload = zip_payload(message)
        pre_requests = PreRequestHooks(add_header_hook, session=s)
        resp_hooks = pre_requests.post(url, data=zipped_payload)
        print(resp_hooks.text)


if __name__ == "__main__":
    with open('loreipsum.txt', mode='r') as fp:
        lines = fp.read()
        with requests.Session() as s:
            sent_message(s, "https://httpbin.org/post", lines)
