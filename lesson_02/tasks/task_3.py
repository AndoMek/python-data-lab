import csv

csv.field_size_limit(2 ** 31 - 1)  # Workaround to avoid _csv.Error: field larger than field limit (131072)


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
        lines_gen = skip_line(fp, start_position, footer)
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


def skip_line(file, start=0, footer=0):
    try:
        for _ in range(start):
            next(file)
    except StopIteration:
        return
    if footer == 0:
        yield from file
    else:
        list_file = list(file)
        len_file = len(list_file)
        iter_file = iter(list_file)
        if len_file > footer:
            len_file -= footer
            try:
                for _ in range(len_file):
                    yield next(iter_file)
            except StopIteration:
                return
        else:
            return


if __name__ == "__main__":
    f = "events.csv"

    with open(f, "r") as fp:
        it = Csv2Dict(
            fp, start_position=1,
            header=False, fieldnames=None,
            delimiter=",", quotechar='"', footer=0
        )
        for row in it:
            print(row)
