from common.types import Component
from common.errors import *
from common.utils import *

class TextBlock(Component):
    """
    Basic printable component that stores block of text, most basic child of Component
    """

    def __init__(self, nrows=1, ncols=1, fixrows=False, fixcols=False,
                 maxrows=10, maxcols=25, wrap=True, wrap_hyphen=True):
        """
        Initializes new text block
        :param nrows: initial rows
        :param ncols: initial cols
        :param fixrows: don't allow resizing of the initial nrows
        :param fixcols: don't allow resizing of the initial ncols
        :param maxcols: maximum cols the block can grow
        :param maxrows: maximum rows the block can grow
        :param wrap: whether to wrap lines that are too long
        :param wrap_hyphen: whether to use hyphen when wrapping line
        """
        # gt_or_raise(nrows, 0,'nrows cannot be 0. {} {}')
        # gt_or_raise(ncols, 0, 'ncols cannot be 0. {} {}')
        self.fixcols=fixcols
        self.fixrows=fixrows
        self.maxcols=maxcols if not fixcols else min(maxcols, ncols)
        self.maxrows=maxrows if not fixrows else min(maxrows, nrows)
        self.wrap=wrap
        self.wrap_hyphen=wrap_hyphen
        self.s = [' '*ncols for _ in range(nrows)]

        super(TextBlock, self).__init__(nrows, ncols)


    def add_line(self, row, line, wrap=None):
        """
        adds a line and returns number of added lines. This comes useful
        when wrapping is turned on and line gets sliced up into several
        rows, this way outside method knows how many rows have been added
        :param row:
        :param line:
        :param wrap: None -> use default, use wrap otherwise
        :return:
        """
        if wrap is None:
            wrap = self.wrap

        if wrap:
            lines = wrap_line(line, self.maxcols, fill_in_last_line=True, use_hyphen=self.wrap_hyphen)
        else:
            lines = [line]

        self[row:row+len(lines),0:len(lines[0])] = lines
        return len(lines)


    def add_lines(self, row, lines, wrap=None):
        """
        adds multiple lines and returns number of actual added lines. This comes useful
        when wrapping is turned on and any of the lines gets sliced up into several
        rows, this way outside method knows how many rows have been added in total
        :param row:
        :param lines:
        :param wrap: None -> use default, use wrap otherwise
        :return:
        """
        all_lines = []
        for line in lines:
            if wrap is None:
                wrap = self.wrap
            if wrap:
                lines = wrap_line(line, self.maxcols, fill_in_last_line=True, use_hyphen=self.wrap_hyphen)
            else:
                lines = [line]

            all_lines += lines

        # make sure all lines have the same len
        all_lines = align_lines_len(all_lines)
        self[row:row+len(all_lines),0:len(all_lines[0])] = all_lines
        return len(all_lines)


    def _resize(self, nrows, ncols):
        """
        Implementation of the template resize method
        :param nrows:
        :param ncols:
        :return: new nrows, new ncols
        """
        if nrows != self.get_nrows() and self.fixrows:
            raise ResizeError('The row count can be changed due to fixrows flag')
        if ncols != self._ncols and self.fixcols:
            raise ResizeError('The col count can be changed due to fixcols flag')

        gte_or_raise(self.maxrows, nrows, 'Number of rows cannot excceed {}, nrows={}', ResizeError)
        gte_or_raise(self.maxcols, ncols, 'Number of cols cannot excceed {}, ncols={}', ResizeError)

        rows_diff = nrows - self._nrows
        cols_diff = ncols - self._ncols

        if nrows <= 0 or ncols <= 0:
            return self.size()

        # add at least one
        if self._nrows == 0 or self._ncols == 0:
            self.s = [[' ']]
            self._nrows = 1
            self._ncols = 1

        # assuming there is at least one row and one column
        if rows_diff < 0:
            self.s = self.s[:len(self.s)+rows_diff]
        if cols_diff < 0:
            self.s = [row[:len(row)+cols_diff] for row in self.s]
        if rows_diff > 0:
            self.s.extend([' ' * self._ncols for _ in range(rows_diff)])
        if cols_diff > 0:
            self.s = [row + ' '*cols_diff for row in self.s]
        return nrows, ncols


    def _get_lines(self):
        """
        Implementation of the template get_lines method
        :return:
        """
        return self.s


    def _get_slice_indices(self, slice_, dim_size):
        """
        Creates indices according to slice
        :param slice_: slice object
        :param dim_size: size of the dimension which is being sliced
        :return: iterable list of int indices
        """
        if isinstance(slice_, int):
            if slice_ < 0:
                return [dim_size+slice_]
            else:
                return [slice_]
        step = 1 if slice_.step is None else slice_.step
        start = 0 if slice_.start is None else slice_.start
        stop = dim_size if slice_.stop is None else slice_.stop
        l = list(range(start, stop, step))
        # add list len to negative indices
        l = [i if i >= 0 else i + len(l) for i in l]
        return l


    def resize_if_necessary(self, maxrow, maxcol):
        """
        Method that resizes if _content doesn't fit
        :param maxrow:
        :param maxcol:
        :return:
        """
        biggerrow = max(maxrow + 1, self._nrows) # add one because it's an index
        biggercol = max(maxcol + 1, self._ncols)
        self.resize(biggerrow, biggercol)


    def resize_if_possible(self, maxrow, maxcol):
        """
        Method that resizes if _content doesn't fit but respects maxrows, maxcols bounds
        :param maxrow:
        :param maxcol:
        :return:
                """
        biggerrow = min(self.maxrows, max(maxrow + 1, self._nrows))  # add one because it's an index
        biggercol = min(self.maxcols, max(maxcol + 1, self._ncols))
        self.resize(biggerrow, biggercol)


    def __getitem__(self, index):
        if isinstance(index, slice):
            return self.s[index]
        elif isinstance(index, tuple) or isinstance(index, int):
            index_ = list(index) if isinstance(index, tuple) else [index]
            n = len(index_)

            if n == 1:
                ret = self.s[index_[0]]
                return ret
            if n == 2:
                if isinstance(index_[0],slice):
                    ret = [self.s[i][index_[1]] for i in self._get_slice_indices(index_[0], self._nrows)]
                    return ret
                else:
                    ret = self.s[index_[0]][index_[1]]
                    return ret
            if n >= 3 or n < 1:
                raise IndexError('Index can have either one or two '
                                 'values. Used index: {}'.format(index_))


    def __setitem__(self, index, value):
        if (not isinstance(index, int) and not isinstance(index, slice) and len(index) == 0) or (len(str(value)) == 0):
            return
        if isinstance(index, slice):
            # call this method again on 2 arguments
            self[index,:] = value
        elif isinstance(index, int):
            # call this method again on 2 arguments
            self[index,:] = value
        elif isinstance(index, tuple) and len(index) == 2:
            index_ = list(index)

            i_indices = self._get_slice_indices(index_[0], self._nrows)
            j_indices = self._get_slice_indices(index_[1], self._ncols)
            self.resize_if_possible(i_indices[-1], j_indices[-1])

            if not isinstance(value, list):
                value = [str(value)]

            for i_iloc,i in enumerate(i_indices):
                row = ''
                j_iloc = 0
                for j in range(self._ncols):
                    if j in j_indices:
                        i_iloc_ = i_iloc % len(value)
                        row += value[i_iloc_][j_iloc % len(value[i_iloc_])]
                        j_iloc += 1
                    else:
                        row += self.s[i][j]
                if i >= len(self.s):
                    break
                self.s[i] = row
        else:
            raise KeyError('unknown index '+str(index))


if __name__ == '__main__':
    b = TextBlock(3, 3, fixrows=False, fixcols=True, maxrows=5, wrap=True)
    b.add_lines(0, ['abcd', 'efgh', 'ijkl'])
    assert b[:, :] == ['ab-', 'cd ', 'ef-', 'gh ', 'ij-']

