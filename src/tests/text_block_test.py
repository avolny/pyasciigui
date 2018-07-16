import pytest
from common.text_block import TextBlock
import numpy.testing as nptest

@pytest.fixture
def text_block1():
    block = TextBlock(3,5,fixrows=True,fixcols=True,wrap=False)

    return block


def test_text_block_1(text_block1):
    b = text_block1
    assert b[:,:] == ['     ','     ','     ']

    b[0] = 'abcde'
    assert b[:, :] == ['abcde', '     ', '     ']
    assert b[0] == 'abcde'
    assert b[0,:] == 'abcde'
    assert b[0,1:4] == 'bcd'
    assert b[0,:1] == 'a'
    assert b[0,-1:] == 'e'
    b[0] = 'abcdefghi'
    assert b[:, :] == ['abcde', '     ', '     ']

    b[1] = '12345'
    assert b[:, :] == ['abcde', '12345', '     ']
    assert b[1] == '12345'
    assert b[:2] == ['abcde','12345']
    assert b[1,:3] == '123'

    b[2,::2] = '=+='
    assert b[:, :] == ['abcde', '12345', '= + =']

    b[0,:2] = ' '
    assert b[0] == '  cde'
    b[0,1:3] = 'x'
    assert b[0] == ' xxde'
    b[0] = 'y'
    assert b[0] == 'yyyyy'
    b[0:2] = 'z'
    assert b[:, :] == ['zzzzz', 'zzzzz', '= + =']
    b[0:2] = 'fghij'
    assert b[:, :] == ['fghij', 'fghij', '= + =']
    b[:,:] = 'x'
    assert b[:, :] == ['xxxxx', 'xxxxx', 'xxxxx']
    b[:,:] = 'ab'
    assert b[:, :] == ['ababa', 'ababa', 'ababa']
    b[:,:] = ['ab','cd']
    assert b[:, :] == ['ababa', 'cdcdc', 'ababa']
    b[:,:] = ['abcdefghijk','cdefgh']
    assert b[:, :] == ['abcde','cdefg','abcde']
    b[:,:] = ['ab','c']
    assert b[:, :] == ['ababa','ccccc','ababa']
    b[:,:] = ' '
    b.fixrows = False
    b.maxrows = 10
    b[0:5:2,::2] = ['123','456','789']
    assert b[:, :] == ['1 2 3','     ','4 5 6','     ','7 8 9']


@pytest.fixture
def text_block2():
    b = TextBlock(3,3,False,True,maxrows=5,wrap=True)
    return b

def test_text_block_2(text_block2):
    b = TextBlock(3,3,fixrows=False,fixcols=True,maxrows=5,wrap=True)
    b.add_line(0,'abcdefg')
    assert b[:,:] == ['ab-','cd-','efg']

    b = TextBlock(3, 3, fixrows=False, fixcols=True, maxrows=5, wrap=True)
    b.add_line(0, 'abcdefgh')
    assert b[:, :] == ['ab-', 'cd-', 'ef-', 'gh ']

    b = TextBlock(3, 3, fixrows=False, fixcols=True, maxrows=5, wrap=True)
    b.add_line(0, 'abcdefghijklmnop')
    assert b[:, :] == ['ab-', 'cd-', 'ef-', 'gh-', 'ij-']

    b = TextBlock(3, 3, fixrows=False, fixcols=True, maxrows=5, wrap=True, wrap_hyphen=False)
    b.add_line(0, 'abcdefghijklmnop')
    assert b[:, :] == ['abc', 'def', 'ghi', 'jkl', 'mno']

    b = TextBlock(3, 3, fixrows=False, fixcols=False, maxcols=1000, wrap=True)
    b.add_line(0, 'abcdefg')
    assert b[:, :] == ['abcdefg','       ','       ']
    b.add_line(1, '12345678')
    assert b[:, :] == ['abcdefg ', '12345678', '        ']


def test_text_block_3():
    b = TextBlock(3, 3, fixrows=False, fixcols=True, maxrows=5, wrap=True)
    b.add_lines(0, ['abcd','efgh','ijkl'])
    assert b[:, :] == ['ab-', 'cd ', 'ef-','gh ','ij-']


