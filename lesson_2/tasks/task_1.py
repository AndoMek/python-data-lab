import csv

csv.field_size_limit(2 ** 31 - 1)  # Workaround to avoid _csv.Error: field larger than field limit (131072)


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
    lines_gen = skip_line(fp, start_position, footer)
    lines = csv.reader(lines_gen, delimiter=delimiter, quotechar=quotechar)

    if header is True:
        try:
            fieldnames = next(lines)
        except StopIteration:
            return
    elif fieldnames is None:
        try:
            row = next(lines)
        except StopIteration:
            return
        fieldnames = ["col%02d" % i for i in range(len(row))]
        yield dict(zip(fieldnames, row))

    for item in lines:
        yield dict(zip(fieldnames, item))


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
