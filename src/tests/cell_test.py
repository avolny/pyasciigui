from common.types import Component
from common.errors import *
from common.utils import *
from common.container import Container
from common.text_block import TextBlock
from common.cell import Cell



def test_cell_1():
    c = Cell()
    assert c[:,:] == ['+-+','| |','+-+']
    c.c[0,0] = 'a'
    assert c[:, :] == ['+-+', '|a|', '+-+']
    c.c[:,:] = 'b'
    assert c[:, :] == ['+-+', '|b|', '+-+']
    c.c.add_line(0,'abc')
    assert c[:, :] == ['+---+', '|abc|', '+---+']

    c = Cell(1, 1,borders=[0]*4)
    c.c[0,0] = 'a'
    assert c.get_lines() == ['a']
    c.c[0:2,0:3] = 'b'
    assert c.get_lines() == ['bbb','bbb']

    c = Cell(1, 1, borders=[1,0,0,0])
    c.add_line('abcd')
    assert c.get_lines() == ['----','abcd']

    c = Cell(1, 1, borders=[0, 1, 0, 0])
    c.add_line('abcd')
    assert c.get_lines() == ['abcd', '----']

    c = Cell(1, 1, borders=[1, 1, 0, 0])
    c.add_line('abcd')
    assert c.get_lines() == ['----', 'abcd', '----']

    c = Cell(1, 1, borders=[1, 1, 1, 0])
    c.add_line('abcd')
    assert c.get_lines() == ['+----', '|abcd', '+----']

    c = Cell(1, 1, borders=[1, 1, 0, 1])
    c.add_line('abcd')
    assert c.get_lines() == ['----+', 'abcd|', '----+']

    c = Cell(1, 1, borders=[0, 0, 0, 1])
    c.add_line('abcd')
    assert c.get_lines() == ['abcd|']

    c = Cell(1, 1, borders=[0, 0, 1, 1])
    c.add_line('abcd')
    assert c.get_lines() == ['|abcd|']

    c = Cell(1, 1, borders=[0, 1, 1, 1])
    c.add_line('abcd')
    assert c.get_lines() == ['|abcd|','+----+']

    c = Cell(1, 1, maxcols=3, maxrows=3, wrap=True)
    c.add_line('abcd')
    c.add_line('')
    c.add_line('efgh')

    assert c.get_lines() == ['+---+','|ab-|','|cd |','|   |','+---+']


    c = Cell(1, 1, wrap=True)
    c.add_line('abcd')
    c.add_line('')
    c.add_fill_line()
    assert c.get_lines() == ['+----+', '|abcd|', '|    |', '|    |', '+----+']
    c.add_fill_column()
    assert c.get_lines() == ['+-----+', '|abcd |', '|     |', '|     |', '+-----+']




