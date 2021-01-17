import csv
from collections import deque
from itertools import islice

csv.field_size_limit(2 ** 31 - 1)  # Workaround to avoid _csv.Error: field larger than field limit (131072)


def csv2dict(fp, start_position=0, header=True, fieldnames=None, delimiter=",", quotechar='"', footer=0):
    """ CSV to Dict Generator

    Args:
        fp: file-like object / stream / Iterator
        start_position: start line if file-like object / stream. Default: 0
        header: Is header exists into file-like object / stream. Default: True
        fieldnames: list or tuple of field name. Default: None
        delimiter: A one-character string used to separate fields. It defaults to ','.
        quotechar: A one-character string used to quote fields containing special characters,
            such as the delimiter or quotechar, or which contain new-line characters. It defaults to '"'
        footer: Positive-integer. Skip last lines in a file-like object / stream. Default: 0

    Requirements:
        1. Read CSV file or iterator of bytes or stream
        2. Start parse file from ``start_position``. E.g. if ``start_position`` = 0 than start from beginning
        header
        3. If ``header`` == True than parse it
        4. If ``header`` == False and fieldnames exists than uses fieldnames
        5. If ``header`` == False and fieldnames is None than generate in format
            [col00, col01, .., col99, .., col100500]
        6. If footer > 0 than skip last ``footer`` lines
        7. Return generator of dictionary, eg:
            { "header_element_1": "csv_element_1",
              "header_element_2": "csv_element_2", .. ,
              "header_element_100500": "csv_element_100500"
            }
        8. If CSV file or iterator of bytes or stream contain only header than generator doesn't return anything

    Samples:
        1. 71 MiB file: https://examples.citusdata.com/tutorial/events.csv

    Additional:
        CSV library: https://docs.python.org/3/library/csv.html
    """
    lines = csv.reader(fp, delimiter=delimiter, quotechar=quotechar)
    try:
        for _ in range(start_position):
            next(lines)
    except StopIteration:
        return
    dictionary = {}
    if header is True:
        header = next(lines)
        for name in header:
            dictionary[name] = None
    elif fieldnames is not None:
        for name in fieldnames:
            dictionary[name] = None
    else:
        row = next(lines)
        for i, field in enumerate(row):
            dictionary["col" + str(i)] = field
    if footer == 0:
        waste = deque(islice(lines, 1), 1)
    else:
        waste = deque(islice(lines, footer), footer)
    for i in lines:
        buff = waste.popleft()
        for field, key in zip(buff, dictionary.keys()):
            dictionary[key] = field
        yield dictionary
        waste.append(i)


if __name__ == "__main__":
    f = "events.csv"

    with open(f, "r") as fp:
        gen = csv2dict(
            fp, start_position=0,
            header=False, fieldnames=None,
            delimiter=",", quotechar='"', footer=0
        )
        for row in gen:
            print(row)