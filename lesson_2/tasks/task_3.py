import csv
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
        pass

    def __iter__(self):
        return self

    def __next__(self):
        pass


if __name__ == "__main__":
    f = "path-to-file.csv"

    with open(f, "rb") as fp:
        it = Csv2Dict(
            fp, start_position=0,
            header=True, fieldnames=None,
            delimiter=",", quotechar='"', footer=0
        )
        for row in it:
            print(row)
