from common.text_block import TextBlock
from common.container import Container
from common.types import ResizeEvent
from common.utils import get_border, wrap_line
from common.cell import Cell
import numpy as np

class ColumnTable(Cell):
    """
    Class representing a column table, that means that
    number of rows of the table in each column can vary.
    Be cautious as it is indexed column first thanks to the
    column property
    """
    def __init__(self, cell_maxrows=12, cell_maxcols=50, cell_borders=(1, 1, 1, 1),
                 cell_content_pad=(0, 0, 0, 0), maxrows=10000, maxcols=5000):
        """
        Instantiates a Table, borders sets type of borders, set 0 for no borders. content_pad sets what happens when no
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
        self.cell_maxrows = cell_maxrows
        self.cell_maxcols = cell_maxcols
        self.cell_borders = cell_borders
        self.cell_content_pad = cell_content_pad
        self.columns = [[self._new_cell()]]

        super(ColumnTable, self).__init__(1, 1, [0] * 4, [0] * 4, maxrows, maxcols, False, False)

    def sync_and_insert_rows(self):
        """
        Syncs col height and inserts a single row at the end of each column
        :return:
        """
        self.sync_columns_height()
        for col in self.columns:
            col.append(self._new_cell())

    def _new_cell(self):
        """
        Creates and returns a cell with default parameters
        :return:
        """
        return Cell(1, 1, maxrows=self.cell_maxrows, maxcols=self.cell_maxcols,
                    borders=self.cell_borders, content_pad=self.cell_content_pad)


    def _add_new_cells_if_necessary(self, col, row):
        """
        adds new columns and cells in such a way,
        that a cell self[col,row] exists
        :param col:
        :param row:
        :return:
        """
        while len(self.columns) < col+1:
            # print 'new col', len(self.columns), col+1
            self.columns.append([self._new_cell()])

        while len(self.columns[col]) < row+1:
            # print 'new row', len(self.columns[col]), row+1
            self.columns[col].append(self._new_cell())


    def add_fill_line(self):
        for col in self.columns:
            col[-1].add_fill_line()


    def add_fill_column(self):
        for row in self.columns[-1]:
            row.add_fill_column()


    def _get_n_column_lines(self, col):
        """
        returns total number of lines printed in a column
        :param colid:
        :return:
        """
        nlines = 1
        last_cell = None
        for i,cell in enumerate(self.columns[col]):
            n = cell.get_nrows()
            if cell.borders[0] == 0:
                n += cell.content_pad[0]
            if cell.borders[1] == 0:
                n += cell.content_pad[1]
            nlines += n - 1
            if last_cell is not None:
                if last_cell.borders[1] != 0 or last_cell.content_pad[1] == 1:
                    nlines -= 1

        return nlines


    def sync_columns_height(self):
        """
        Columns of the table can have different bottom level because the cells
        don't have to fit into a rectangular grid, only to a vertical grid.
        This method provides a way to delimit all the columns on the same actual row
        so all the borders will be in line even though the cells end at different points
        the furthest cell border level is used.
        :return:
        """
        max_lines = max([self._get_n_column_lines(i) for i in range(len(self.columns))])
        for i,col in enumerate(self.columns):
            while self._get_n_column_lines(i) < max_lines:
                col[-1].add_fill_line()


    def _get_cell_width(self, cell):
        """
        returns number of cols in a cell accounting for its content_pad
        :return:
        """

        return cell.get_ncols() + \
               (cell.content_pad[2] if cell.borders[2] == 0 else 0) + \
               (cell.content_pad[3] if cell.borders[3] == 0 else 0)


    def sync_columns_width(self):
        """
        make all the rows within each column the same width
        :return:
        """
        for i,col in enumerate(self.columns):
            max_width = max([self._get_cell_width(cell) for cell in col])
            for cell in col:
                while self._get_cell_width(cell) < max_width:
                    cell.add_fill_column()


    def _get_lines(self):
        self._render_table()
        return super(ColumnTable, self)._get_lines()


    def get_nrows(self):
        self._render_table()
        return super(ColumnTable, self).get_nrows()


    def get_ncols(self):
        self._render_table()
        return super(ColumnTable, self).get_ncols()


    def _render_table(self):
        self.sync_columns_width()
        self.sync_columns_height()

        j = 0
        for col in self.columns:
            i = 0
            for cell in col:
                i1 = i + (cell.content_pad[0] if cell.borders[0] == 0 else 0)
                i2 = i1 + cell.get_nrows()
                j1 = j + (cell.content_pad[2] if cell.borders[2] == 0 else 0)
                j2 = j1 + cell.get_ncols()
                self.c[i1:i2,j1:j2] = cell.get_lines()
                i = i2 + (cell.content_pad[1] if cell.borders[1] == 0 else 0) - 1

            j = j2 + (col[-1].content_pad[3] if cell.borders[3] == 0 else 0) - 1


    def get_nrows(self):
        # self._render_table()
        return super(ColumnTable, self).get_nrows()


    def get_ncols(self):
        # self._render_table()
        return super(ColumnTable, self).get_ncols()


    def get_cell(self, col, row):
        self._add_new_cells_if_necessary(col, row)
        return self.columns[col][row]


    def set_cell(self, col, row, cell):
        if isinstance(cell, ColumnTable):
            cell._render_table()
        self._add_new_cells_if_necessary(col, row)
        self.columns[col][row] = cell






if __name__ == '__main__':
    # t = ColumnTable()
    # t.get_cell(0, 0).add_line('a')
    # t.get_cell(0, 1).add_line('b')
    # # t._render_table()
    # t2 = ColumnTable()
    # t2.get_cell(0, 0).add_line('c')
    # t2.set_cell(1, 0, t)
    # # t.get_cell(0, 0).add_line('a')
    # # t.get_cell(0, 0).add_fill_line()
    # # t.get_cell(1, 0).add_line('ab')
    # # t.get_cell(1, 1).add_line('cd')
    # print t2
    # # print t
    # t = ColumnTable()
    # t.get_cell(0,0).add_line('abc')
    # t.get_cell(1,0).add_line('def')
    # # t.get_cell(2,0).add_line('ghi')

    t = ColumnTable()
    t.get_cell(0, 0).add_line('a')
    t.get_cell(1, 0).add_line('b')
    t.get_cell(2, 0).add_line('c')
    t.get_cell(0, 1).add_line('abcd')
    print t
