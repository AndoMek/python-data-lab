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