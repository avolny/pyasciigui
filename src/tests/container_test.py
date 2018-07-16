from common.types import Component
from common.errors import *
from common.utils import *
from common.container import Container
from common.text_block import TextBlock


def test_container_1():
    c = Container()
    b = TextBlock(1,1)
    c.add_component(b, 1, 1)

    assert c.size() == (2,2)

    b.resize(3,3)
    assert c.size() == (4,4)

    b[3,3] = 'x'
    assert c.size() == (5,5)
    assert c[4,4] == 'x'


def test_container_2():
    c = Container()
    b = TextBlock(1,1,maxcols=3)
    c.add_component(b, 1, 1)

    b2 = TextBlock(1,1,maxcols=3)
    c.add_component(b2, 1, 0, b, 'botleft')

    b.add_line(0, 'abcd')
    b2.add_line(0, 'efgh')
    assert c[:,:] == ['    ',' ab-',' cd ',' ef-',' gh ']
