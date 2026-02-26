import sys
import os
import pytest

sys.path.append(os.path.abspath('./..'))

from models.helpers.Printing import Printing

# sys.path.append(os.path.abspath('/usr/local/bin'))
# import pytest

@pytest.mark.printing
@pytest.mark.parametrize('set, expected', [
    (1, "\u2022"),
    (2, "\u25CF"),
    (3, "\u2B24"),
    (None, "\u25CF"),
    (84984, "\u25CF"),
])
def test_black_dot_function(set, expected):
    assert Printing.blackDot(set) == expected

@pytest.mark.printing
@pytest.mark.parametrize('set, expected', [
    (['a', '3', 'f', ''], 1),
    (['sodif', 'sof', 1561], 5),
    (['fef', 'sof', 561], 3),
    ([], 0)
])    
def test_get_longest_item_lenght(set, expected):
    assert Printing.getLengthLongestListItem(set) == expected

@pytest.mark.printing
def test_alignDotInCenter():
    assert Printing.alignDotInCenter(1) == Printing.blackDot()
    assert Printing.alignDotInCenter(2) == '_'+Printing.blackDot()
    assert Printing.alignDotInCenter(3) == '_' + Printing.blackDot() + '_'
    assert Printing.alignDotInCenter(4) == '__' + Printing.blackDot() + '_'
    assert Printing.alignDotInCenter(5) == '__' + Printing.blackDot() + '__'

@pytest.mark.printing
@pytest.mark.parametrize('set, expected, param', [
    (['apple', 'banana', 'cocoa', 'marakuija'], 'apple|banana|cocoa|marakuija', None),
    (['apple', 'banana', 'cocoa', 'marakuija'], 'apple | banana | cocoa | marakuija', ' | '),
    (['apple', 'banana', 1, 'marakuija'], 'apple / banana / 1 / marakuija', ' / '),
    (('apple', 'banana', 1, 'some', 'marakuija'), 'apple / banana / 1 / some / marakuija', ' / '),
])
def test_convertListToString(set, expected, param):
    if param is None:
        string = Printing.convertListToString(set)
    else:
        string = Printing.convertListToString(set, param)

    assert type(string) == str
    assert string == expected

def test_blackDot_Exception():

    # with pytest.raises(Exception):
        # blackDot('some string')
    pass
