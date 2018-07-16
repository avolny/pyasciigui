


def get_border(id, len, hor=True):
    """
    Draws borders
    :param id: {'0': ' ', '1': '-', '2': '='}/{'0': ' ', '1': '|', '2': 'I'}
    :param len:
    :param hor: True for horizontal borders, False for vertical
    :return: str/list(str)
    """

    chars_hor = {0: ' ', 1: '-', 2: '='}
    chars_ver = {0: ' ', 1: '|', 2: 'I'}
    corners = {0: ' ', 1: '+', 2: '+'}
    def border(char, corner):
        return corner + char*(len-2) + corner if hor else [corner] + [char for _ in range(len-2)] + [corner]

    if hor: # horizontal borders
        return border(chars_hor[id], corners[id])
    else:   # vertical borders
        return border(chars_ver[id], corners[id])


def wrap_line(line, maxlen, fill_in_last_line=True, use_hyphen=True):
    """
    Wrap a line according to params
    :param line: str
    :param maxlen: maximum number of columns
    :param fill_in_last_line: fill in last line with spaces to match the rest
    :param use_hyphen: use hyphen when splitting lines
    :return: list of splitted lines
    """
    ix = 0
    lines = []
    line_ = line
    hyphen = '-' if use_hyphen else ''
    while len(line_) > maxlen:
        lines.append(line[ix:ix + maxlen - len(hyphen)] + hyphen)
        ix += maxlen - len(hyphen)
        line_ = line[ix:]
    max_line_len = max([len(l) for l in lines] + [len(line)])
    if fill_in_last_line:
        line_ = line_ + ' '*(max_line_len-len(line_))
    lines.append(line_)

    return lines


def align_lines_len(lines):
    """
    Fills in spaces into lines such that they have the same length
    :param lines: list of str
    :return: list of str with all rows of equal length
    """
    maxlen = max([len(line) for line in lines])
    lines = [line + ' '*(maxlen-len(line)) for line in lines]
    return lines