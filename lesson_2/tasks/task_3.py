import csv
from collections import deque
from itertools import islice

csv.field_size_limit(2**31 - 1)  # Workaround to avoid _csv.Error: field larger than field limit (131072)


class Csv2Dict:
    """ CSV to Dict Iterator

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
        7. Iterator return of dictionary, eg:
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

    def __init__(self, fp, start_position=0, header=True,
                 fieldnames=None, delimiter=",", quotechar='"', footer=0):
        self.lines = csv.reader(fp, delimiter=delimiter, quotechar=quotechar)
        try:
            for _ in range(start_position):
                next(self.lines)
        except StopIteration:
            return
        self.dictionary = {}
        if header is True:
            header = next(self.lines)
            for name in header:
                self.dictionary[name] = None
        elif fieldnames is not None:
            for name in fieldnames:
                self.dictionary[name] = None
        else:
            row = next(self.lines)
            for i, field in enumerate(row):
                self.dictionary["col" + str(i)] = field
        if footer == 0:
            self.waste = deque(islice(self.lines, 1), 1)
        else:
            self.waste = deque(islice(self.lines, footer), footer)

    def __iter__(self):
        return self

    def __next__(self):
        item = next(self.lines)
        buff = self.waste.popleft()
        for field, key in zip(buff, self.dictionary.keys()):
            self.dictionary[key] = field
        self.waste.append(item)
        return self.dictionary


if __name__ == "__main__":
    f = "walmart_stock.csv"

    with open(f, "r") as fp:
        it = Csv2Dict(
            fp, start_position=0,
            header=True, fieldnames=None,
            delimiter=",", quotechar='"', footer=1200
        )
        for row in it:
            print(row)
