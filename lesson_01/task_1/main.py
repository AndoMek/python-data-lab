def head(filepath: str, n: int):
    """ Read file ``filepath`` in text mode and print beginning ``n`` lines of file

    Requirements:
        1. Open file ``filepath`` in text mode and read first ``n`` lines and output to console (print)
        2. If ``n`` == 0 then shouldn't output anything to console
        3. If file ``filepath`` are empty than shouldn't output anything to console
        4. If ``n`` greater than actual lines than output to console whole file content

    :param filepath: path to text file
    :param n: number of line to output. Integer great or equal zero
    """


if __name__ == "__main__":
    import os
    ROOT = os.path.dirname(__file__)

    loreipsum_path = os.path.join(ROOT, "loreipsum.txt")
    blank_path = os.path.join(ROOT, "blank.txt")

    # Should print first 10 lines. Equal to GNU `head` command
    # head -n 10 loreipsum.txt
    head(loreipsum_path, 10)

    # Should print nothing. Equal to GNU `head` command
    # head -n 0 loreipsum.txt
    head(loreipsum_path, 0)

    # Should print whole file line by line. Equal to GNU `head` command
    # head -n 100500 loreipsum.txt
    head(loreipsum_path, 100500)

    # # Should print nothing (file is empty). Equal to GNU `head` command
    # head -n 10 blank.txt
    head(blank_path, 10)
