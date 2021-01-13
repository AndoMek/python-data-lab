def tac(filepath: str):
    """ Read file ``filepath`` in text mode and reversing the records (lines by default) in each separately

    Requirements:
        1. Open file ``filepath`` in text mode and read last ``n`` lines and output to console (print)
        2. If file ``filepath`` are empty than shouldn't output anything to console
        3. Lines content should output in direct order (not reversed)

    :param filepath: path to text file
    :param n: number of line to output. Integer great or equal zero
    """
    lines = []
    if os.stat(filepath).st_size != 0:
        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f]
    for i in reversed(lines):
        print(i)

if __name__ == "__main__":
    import os
    ROOT = os.path.dirname(__file__)

    loreipsum_path = os.path.join(ROOT, "loreipsum.txt")
    blank_path = os.path.join(ROOT, "blank.txt")

    # Should print all lines in reversed order. Equal to GNU `tac` command
    # tac loreipsum.txt
    tac(loreipsum_path)

    # Should print nothing (file is empty). Equal to GNU `tac` command
    # tac blank.txt
    tac(blank_path)
