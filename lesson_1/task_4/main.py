def nl(filepath: str, v: int = 1, s: str = "\t\t"):
    """ Read file ``filepath`` in text mode, numbering lines and output with original line

    Requirements:
        1. Open file ``filepath`` in text mode and output to console number of line + separator + original line
        2. If file ``filepath`` are empty than shouldn't output anything to console

    :param filepath: path to text file
    :param v: first line number
    :param s: separator between number and line
    """
    lines = []
    if os.stat(filepath).st_size != 0:
        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f]
    for i,line in enumerate(lines):
        print(str(i+v)+s+line)


if __name__ == "__main__":

    import os
    ROOT = os.path.dirname(__file__)

    loreipsum_path = os.path.join(ROOT, "loreipsum.txt")
    blank_path = os.path.join(ROOT, "blank.txt")

    # Should print whole file with numbers of string. Equal to GNU `nl` command
    # nl loreipsum.txt -w 1
    nl(loreipsum_path)

    # Should print whole file with numbers of lines with separator ": ". Equal to GNU `nl` command
    # nl loreipsum.txt -s ': ' -w 1
    nl(loreipsum_path, s=": ")

    # Should print whole file with numbers of lines and numeration start from 42. Equal to GNU `nl` command
    # s.stat(filepath).st_size
    nl(loreipsum_path, v=42)

    # Should print nothing (file is empty). Equal to GNU `nl` command
    # nl blank.txt -w 1
    nl(blank_path)
