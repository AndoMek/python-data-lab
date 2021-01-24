import csv
from collections import deque
from itertools import islice
import requests

csv.field_size_limit(2 ** 31 - 1)

""" Task 2: Remote CSV to Dict Iterator

Requirements:
    1. Implement class DictRemoteCsvReader
    2. Class should implement Iterator protocol
    3. Class should read data by HTTP(s) protocol
    4. Class Arguments:
        url: path to csv file
        start_position: start line if file-like object / stream. Default: 0
        header: Is header exists into file-like object / stream. Default: True
        fieldnames: list or tuple of field name. Default: None
        delimiter: A one-character string used to separate fields. It defaults to ','.
        quotechar: A one-character string used to quote fields containing special characters,
            such as the delimiter or quotechar, or which contain new-line characters. It defaults to '"'
        footer: Positive-integer. Skip last lines in a file-like object / stream. Default: 0

    5. Additional Requirement
        a. Iterator should return dictionary object
        b. Start parse file from ``start_position`` line
        c. If footer > 0 than skip last ``footer`` lines
        c. If ``header`` == True than parse it from file
        d. If ``header`` == False and fieldnames exists than uses fieldnames
        d. If ``header`` == False and fieldnames is None than generate fieldnames in format
            [col00, col01, .., col99, .., col100500]

Nice To Have:
    1. Implement Context Manager Protocol and work both implementation
            a. Without context manager
            csv_dict = DictRemoteCsvReader(...)
            for x in csv_dict:
                print(x)

            b. With context manager
            with DictRemoteCsvReader(...) as csv_dict
                for x in csv_dict:
                    print(x)
"""


class NotFoundError(Exception):
    """NBRB data is blank"""
    pass


def skip_line(file, start: int, footer: int):
    """Skip first and last lines
    Args
        file: file-like object / stream / Iterator
        start: number of first lines to skip. Int. Default 0
        footer: number of last lines to skip. Integer. Default 0
    Returns
        Generator
    """

    try:
        for _ in range(start):
            next(file)
    except StopIteration:
        return
    if footer == 0:
        yield from file
    else:
        if footer == 0:
            waste = deque(islice(file, 1), 1)
        else:
            waste = deque(islice(file, footer), footer)
        for i in file:
            yield waste.popleft()
            waste.append(i)
        if footer == 0:
            yield waste.popleft()


class DictReader:
    """Read via HTTP and Convert csv row to  dict"""

    def __init__(self, fp: str, start_position: int = 0, header: bool = True,
                 fieldnames: tuple = None, delimiter: str = ",", quotechar: str = '"', footer: int = 0):
        self.url_path = fp
        try:
            self.fp = requests.get(self.url_path, stream=True)
        except requests.exceptions.MissingSchema:
            raise NotFoundError(f"Can not find URL {self.url_path}")
        self.closed = False
        if self.fp.status_code != 200:
            raise requests.HTTPError(f"Can not download csv file from {self.url_path}")
        self.fp_iter = self.fp.iter_lines(decode_unicode=True)
        lines_gen = skip_line(self.fp_iter, start_position, footer)
        self.lines = csv.reader(lines_gen, delimiter=delimiter, quotechar=quotechar)
        self.first = False
        if header is True:
            try:
                self.fieldnames = next(self.lines)
            except StopIteration:
                return
        elif fieldnames is None:
            try:
                row = next(self.lines)
            except StopIteration:
                return
            self.fieldnames = ["col%02d" % i for i in range(len(row))]
            self.first_row = dict(zip(self.fieldnames, row))
            self.first = True

    def __iter__(self):
        return self

    def __next__(self):
        if self.first is True:
            self.first = False
            return self.first_row
        item = next(self.lines)
        return dict(zip(self.fieldnames, item))

    def close(self):
        """Close connection"""
        if self.closed:
            raise OSError(f"Connection {self.url_path!r} already closed")
        self.closed = True
        self.fp.close()

    def __enter__(self):
        if self.closed:
            raise OSError(f"Connection {self.url_path!r} closed")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.closed:
            self.close()


if __name__ == "__main__":
    f = "https://examples.citusdata.com/tutorial/events.csv"
    it = DictReader(
        f, start_position=0,
        header=False, fieldnames=None,
        delimiter=",", quotechar='"', footer=0
    )
    for row in it:
        print(row)
    it.close()
    with DictReader(f, start_position=0,
                    header=False, fieldnames=None,
                    delimiter=",", quotechar='"', footer=100) as f:
        for row in f:
            print(row)
