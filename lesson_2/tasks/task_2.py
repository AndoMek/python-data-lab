from decimal import Decimal as _D
from datetime import datetime as _dt
from tempfile import TemporaryFile as _TF
from datetime import time as _t
from datetime import date as _d

"""
1. Create class JSONEncoderExtended which serialise object to json and inheritance of json.JSONEncoder
2. Implement two functions:
    json_dumps(obj, **kw) - convert Python objects into в json-string, the same manner as json.dumps()
        obj: object for convert
        kw: key-words arguments same as json.dumps() has

    json_dump(obj, fp, **kw) - convert Python objects into в json-string and save into file-like object
        the same manner as json.dump()
        obj: object for convert
        fp: file-like object
        kw: key-words arguments same as json.dump() has

3. Convert rules:
    None -> JSON null
    int -> JSON number
    float -> JSON number
    bool -> JSON boolean
    list -> JSON array
    tuple -> JSON array
    dict -> JSON object
    str -> JSON string

    decimal.Decimal -> JSON number
    set -> JSON array
    datetime.datetime -> JSON string (in iso ISO-8601 format "YYYY-MM-DD HH:mm:ss.SSSSSS")
    datetime.date -> JSON string (in iso ISO-8601 format "YYYY-MM-DD")
    datetime.time -> JSON string (in iso в ISO-8601 format "HH:mm:ss.SSSSSS")
    In other cases ``raise TypeError``

4. You not limited to use only datatime library. You can use any library, like python-dateutil or pendulum
    However better to use datetime library for this task
    https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior

"""

import json


class JSONEncoderExtended(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, _dt):
            return o.strftime("%Y-%m-%d %H:%M:%S.%f")
        if isinstance(o, _d):
            return o.strftime("%Y-%m-%d")
        if isinstance(o, _t):
            return o.strftime("%H:%M:%S.%f")
        if isinstance(o, _D):
            return str(o)
        if isinstance(o, (list, tuple, set)):
            o = list(o)
            for i in range(len(o)):
                o[i] = self.default(o[i])
            return o
        if isinstance(o, dict):
            for key in list(o):
                o[key] = self.default(o[key])
            return o
        return super(JSONEncoderExtended, self).default(o)


def json_dumps(obj, **kw):
    return json.dumps(obj, cls=JSONEncoderExtended, **kw)


def json_dump(obj, fp, **kw):
    return json.dump(obj, fp, cls=JSONEncoderExtended, **kw)


if __name__ == "__main__":

    import logging

    logging.basicConfig(level=logging.INFO)

    objects = [
        1,
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt",
        None,
        True,
        [1, "Lorem ipsum", None, False, ],
        {
            "ccc": 1,
            "b": ["Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt",
                  {"c": None, "d": True}
                  ],
            "1": None,
            "e": {
                "date": _dt.now().date(),
                "datetime": _dt.now(),
                "time": _dt.now().time()
            },
            "2": (1, 2, None, 3, 4,),
            # "acdc": {1, 2, 2, 2, 1, 5},
            "numbers": {
                "int": 42,
                "loooooooong_int": 100 ** 100,
                "float": 0.333 + 0.333 + 0.333,
                "decimal": _D("0.333") + _D("0.333") + _D("0.333"),
            },
        },
    ]

    for item in objects:
        logging.info("Cast object to json-string")
        try:
            logging.info("%s\n", json_dumps(item, indent=2))
        except TypeError as ex:
            logging.error("Failed: %s\n", ex)

        logging.info("Cast object to JSON and save in file-like object")
        with _TF("wt") as tf:
            try:
                json_dump(item, tf, indent=2)
            except TypeError as ex:
                logging.error("Failed: %s\n", ex)
            else:
                logging.info("Success\n")
