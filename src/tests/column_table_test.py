from common.types import Component
from common.errors import *
from common.utils import *
from common.container import Container
from common.text_block import TextBlock
from common.cell import Cell
from column_table.column_table import ColumnTable



def test_table_1():
    t = ColumnTable()
    t.get_cell(0,0).add_line('abc')
    assert t.get_lines() == ['+---+','|abc|','+---+']

    t = ColumnTable()
    t.get_cell(0, 0).add_line('a')
    t.get_cell(0, 1).add_line('ab')
    assert t.get_lines() == ['+--+', '|a |', '+--+', '|ab|', '+--+']

    t = ColumnTable()
    t.get_cell(0, 0).add_line('a')
    t.get_cell(1, 0).add_line('ab')
    t.get_cell(1, 0).add_line('cd')
    assert t.get_lines() == ['+-+--+', '|a|ab|', '| |cd|', '+-+--+']

    t = ColumnTable()
    t.get_cell(0, 0).add_line('a')
    t.get_cell(0, 0).add_fill_line()
    t.get_cell(1, 0).add_line('ab')
    t.get_cell(1, 1).add_line('cd')
    assert t.get_lines() == ['+-+--+', '|a|ab|', '| +--+','| |cd|','+-+--+']

def test_table_2():
    t = ColumnTable()
    t.set_cell(0,0,Cell(borders=[0]*4,content_pad=[0]*4))
    t.get_cell(0,0).add_line('a')
    assert t._get_n_column_lines(0) == 1

    t = ColumnTable()
    t.set_cell(0, 0, Cell(borders=[0] * 4, content_pad=[0] * 4))
    t.get_cell(0, 0).add_line('a')
    t.get_cell(0, 0).add_line('a')
    assert t._get_n_column_lines(0) == 2

    t = ColumnTable()
    t.get_cell(0, 0).add_line('a')
    assert t._get_n_column_lines(0) == 3

    t = ColumnTable()
    t.get_cell(0, 0).add_line('a')
    t.get_cell(0, 0).add_line('b')
    assert t._get_n_column_lines(0) == 4

    t = ColumnTable()
    t.get_cell(0, 0).add_line('a')
    t.get_cell(0, 1).add_line('b')
    assert t._get_n_column_lines(0) == 5

    t = ColumnTable()
    t.get_cell(0, 0).add_line('a')
    assert t._get_cell_width(t.get_cell(0,0)) == 3

    t = ColumnTable()
    t.get_cell(0, 0).add_line('ab')
    assert t._get_cell_width(t.get_cell(0, 0)) == 4

    t = ColumnTable()
    t.get_cell(0, 0).add_line('a')
    t.get_cell(1, 0).add_line('ab')
    t._render_table()
    assert t._get_cell_width(t) == 6

def test_table_3():
    t = ColumnTable()
    t.get_cell(0, 0).add_line('a')
    t.get_cell(1, 0).add_line('b')
    t.get_cell(2, 0).add_line('c')
    assert t.get_lines() == ['+-+-+-+','|a|b|c|','+-+-+-+']








