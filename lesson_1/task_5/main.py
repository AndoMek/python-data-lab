def wc(filepath: str):
    """ Read file ``filepath`` in text mode count lines

    Requirements:
        1. Open file ``filepath`` in text mode count number of lines in file
        2. If file ``filepath`` are empty than number than return 0

    :param filepath: path to text file
    :return Number of lines in file
    """
    try:
        length = len(open(filepath).readlines())
        return length
    except:
        return None

if __name__ == "__main__":
    import os
    ROOT = os.path.dirname(__file__)

    loreipsum_path = os.path.join(ROOT, "loreipsum.txt")
    blank_path = os.path.join(ROOT, "blank.txt")

    # Should print whole file with numbers of string. Equal to GNU `wc` command
    # cat loreipsum.txt | wc -l
    print(wc(loreipsum_path))

    # Should print whole file with numbers of lines with separator ": ". Equal to GNU `wc` command
    # cat blank.txt | wc -l
    print(wc(blank_path))
