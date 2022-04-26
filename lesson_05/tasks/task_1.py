import csv
from collections import deque
from itertools import islice

csv.field_size_limit(2 ** 31 - 1)
""" Task 1: CSV to Dict Iterator with context manager support

Requirements:
    1. Implement class DictCsvReader
    2. Class should implement Iterator protocol
    3. Class should implement Context Manager Protocol and should work both implementation
            a. Without context manager
            csv_dict = DictCsvReader(...)
            for x in csv_dict:
                print(x)

            b. With context manager
            with DictCsvReader(...) as csv_dict
                for x in csv_dict:
                    print(x)

    4. Class Arguments:
        filepath: path to csv file
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
"""


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
    """Read file and Convert csv row to  dict"""

    def __init__(self, fp: str, start_position: int = 0, header: bool = True,
                 fieldnames: tuple = None, delimiter: str = ",", quotechar: str = '"', footer: int = 0):
        """ Initialize DictReader object

        Args:
            filepath: Path to file. String
            start_position: number of first lines to skip. Int. Default 0
            header: Header in file . Boolean. Default True.
            filednames: Header name. tuple of string. Default None.
            delimiter: separator for field. String. Default ','
            quoter: Separator for big filed with delimiter. Default '"'
            footer: number of last lines to skip. Integer. Default 0
        """
        self.filepath = fp
        self.file = open(self.filepath, "r")
        self.lines = iter([])
        self.closed = False
        self.fieldnames = []
        self.first_row = dict()
        self.first = False
        self.start_position = start_position
        self.header = header
        self.fieldnames = fieldnames
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.footer = footer
        self.first_run = True

    def preparatory_work(self):
        self.lines = skip_line(self.file, self.start_position, self.footer)
        self.lines = csv.reader(self.lines, delimiter=self.delimiter, quotechar=self.quotechar)
        if self.header is True:
            try:
                self.fieldnames = next(self.lines)
            except StopIteration:
                return
        elif self.fieldnames is None:
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
        if self.first_run:
            self.first_run = False
            self.preparatory_work()
        if self.first is True:
            self.first = False
            return self.first_row
        item = next(self.lines)
        return dict(zip(self.fieldnames, item))

    def close(self):
        """Close file"""
        if self.closed:
            raise OSError(f"File {self.filepath!r} already closed")
        self.closed = True
        self.file.close()

    def __enter__(self):
        if self.closed:
            raise OSError(f"File {self.filepath!r} closed")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.closed:
            self.close()


if __name__ == "__main__":
    f = "../../lesson_2/tasks/events.csv"
    it = DictReader(
        f, start_position=0,
        header=False, fieldnames=None,
        delimiter=",", quotechar='"', footer=0
    )
    for row in it:
        print(row)
    it.close()
    it.close()
    with DictReader(
            f, start_position=0,
            header=False, fieldnames=None,
            delimiter=",", quotechar='"', footer=0
    ) as f:
        for row in f:
            print(row)
