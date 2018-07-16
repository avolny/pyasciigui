from common.text_block import TextBlock
from common.container import Container
from common.types import ResizeEvent
from common.utils import get_border, wrap_line

class Cell(Container):
    def __init__(self, nrows=1, ncols=1, borders=(1, 1, 1, 1), content_pad=(0, 0, 0, 0), maxrows=10000, maxcols=1000, fixrows=False, fixcols=False, wrap=True, wrap_hyphen=True):
        """
        Instantiates a Cell, borders sets type of borders, set 0 for no borders. content_pad sets what happens when no
        borders is used, 1 means that
        :param nrows:
        :param ncols:
        :param borders:
        :param content_pad:
        :param maxrows:
        :param maxcols:
        :param fixrows:
        :param fixcols:
        :param wrap:
        :param wrap_hyphen:
        """
        self.borders = borders
        self.isnt_border = [1 if border == 0 else 0 for border in borders]
        self.content_pad = content_pad

        super(Cell, self).__init__(nrows+2, ncols+2, fixrows, fixcols, maxrows+2, maxcols+2, wrap)

        self._content = TextBlock(nrows, ncols, fixrows, fixcols, maxrows, maxcols, wrap, wrap_hyphen)
        self.c = self._content
        orient = ['top','bot','left','right']
        self._borders = [CellBorder(orient[i], borders[i], self._content, fixrows, fixcols, maxrows+2, maxcols+2)
                         for i in range(4)]

        self.add_component(self._content, 1, 1)
        self.add_component(self._borders[0], -1, -1, self._content, 'topleft') # TOP
        self.add_component(self._borders[1], 1, -1, self._content, 'botleft')  # BOT
        self.add_component(self._borders[2], -1, -1, self._content, 'topleft')  # LEFT
        self.add_component(self._borders[3], -1, 1, self._content, 'topright')  # RIGHT
        self.rowix = 0


    def get_nrows(self):
        return self._nrows - self.isnt_border[0] - self.isnt_border[1]


    def get_ncols(self):
        return self._ncols - self.isnt_border[2] - self.isnt_border[3]


    def add_fill_line(self):
        """
        adds an empty line at the bottom of the cell, can be overridden for custom behavior
        :return:
        """
        self._content[self._content.get_nrows()] = ' '


    def add_fill_column(self):
        """
        adds an empty column at the rightmost of the cell, can be overridden for custom behavior
        :return:
        """
        self._content[:,self._content.get_ncols()] = ' '


    def add_line(self, line=''):
        """
        adds a line to the next row of the cell
        :param line:
        :return:
        """
        if line == '':
            line = ' '
        self.rowix += self.c.add_line(self.rowix, line)


    def _get_lines(self):
        u = self.isnt_border[0]
        d = self._nrows - self.isnt_border[1]
        l = self.isnt_border[2]
        r = self._ncols - self.isnt_border[3]

        return self[u:d,l:r]


class CellBorder(TextBlock):
    def __init__(self, type='top', id=1, content=None, fixrows=False, fixcols=False, maxrows=12, maxcols=27):
        self.type = type
        self.id = id
        content.add_resize_listener_func(self.content_resize_performed)

        super(CellBorder, self).__init__(1, 1, fixrows, fixcols, maxrows, maxcols)

        self.content_resize_performed(ResizeEvent(content, content.size(), content.size()))


    def content_resize_performed(self, e):
        content = e.o
        old_size = e.old_size
        new_size = e.new_size
        newrows, newcols = new_size
        newrows += 2
        newcols += 2

        if self.type == 'top':
            self[0, 0:newcols]  = get_border(self.id, newcols, True)
        elif self.type == 'bot':
            self[-1, 0:newcols] = get_border(self.id, newcols, True)
        elif self.type == 'left':
            self[0:newrows, 0]  = get_border(self.id, newrows, False)
        elif self.type == 'right':
            self[0:newrows, -1] = get_border(self.id, newrows, False)
        else:
            raise ValueError('unknown borders type "{}"'.format(type))

if __name__ == '__main__':
    c = Cell(1, 1, maxcols=3, maxrows=3, wrap=True)
    c.add_line('abcd')
    c.add_line('')
    c.add_line('efgh')

    print c


