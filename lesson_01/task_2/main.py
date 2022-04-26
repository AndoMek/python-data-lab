def tail(filepath: str, n: int):
    """ Read file ``filepath`` in text mode and print endings ``n`` lines of file

    Requirements:
        1. Open file ``filepath`` in text mode and read last ``n`` lines and output to console (print)
        2. If ``n`` == 0 then shouldn't output anything to console
        3. If file ``filepath`` are empty than shouldn't output anything to console
        4. If ``n`` greater than actual lines than output to console whole file content
        5. Output in the order of data in the file

    :param filepath: path to text file
    :param n: number of line to output. Integer great or equal zero
    """
    try:
        length = len(open(filepath).readlines())
    except (FileNotFoundError, IsADirectoryError):
        print(f'tail: cannot open {filepath} for reading: No such file or directory')
        return None
    if n > 0 or os.stat(filepath).st_size != 0:
        with open(filepath, 'r') as f:
            for i in range(length):
                line = next(f).strip()
                if i >= length - n:
                    print(line)


if __name__ == "__main__":
    import os

    ROOT = os.path.dirname(__file__)

    loreipsum_path = os.path.join(ROOT, "loreipsum.txt")
    blank_path = os.path.join(ROOT, "blank.txt")

    # Should print last 10 lines. Equal to GNU `tail` command
    # tail -n 10 loreipsum.txt
    tail(loreipsum_path, 10)

    # Should print nothing. Equal to GNU `tail` command
    # tail -n 0 loreipsum.txt
    tail(loreipsum_path, 0)

    # Should print whole file line by line. Equal to GNU `tail` command
    # tail -n 100500 loreipsum.txt
    tail(loreipsum_path, 100500)

    # Should print nothing (file is blank). Equal to GNU `tail` command
    # tail -n 10 blank.txt
    tail(blank_path, 10)
