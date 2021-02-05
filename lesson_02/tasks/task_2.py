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
    """Extended JSON encoder"""
    pass


def json_dumps(obj, **kw):
    """
    Serialize ``obj`` as a JSON formatted ``str``. Use BaseJSONEncoder
    """
    pass


def json_dump(obj, fp, **kw):
    """
    Serialize ``obj`` as a JSON formatted stream to ``fp`` (a ``.write()``-supporting file-like object).
    """
    pass


if __name__ == "__main__":
    from decimal import Decimal as _D
    from datetime import datetime as _dt
    from tempfile import TemporaryFile as _TF

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
            "acdc": {1, 2, 2, 2, 1, 5},
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
