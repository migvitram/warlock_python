import pytest
from libraries.printing.PrintingBasic import PrintingBasic
from libraries.printing.PrintingCharts import PrintingCharts

@pytest.mark.printing
@pytest.mark.parametrize('set, expected', [
    (1, "\u2022"),
    (2, "\u25CF"),
    (3, "\u2B24"),
    (None, "\u25CF"),
    (84984, "\u25CF"),
])
def test_black_dot_function(set, expected):
    assert PrintingCharts.blackDot(set) == expected

@pytest.mark.printing
@pytest.mark.parametrize('set, expected', [
    (['a', '3', 'f', ''], 1),
    (['sodif', 'sof', 1561], 5),
    (['fef', 'sof', 561], 3),
    ([], 0)
])    
def test_get_longest_item_lenght(set, expected):
    assert PrintingCharts.getLengthLongestListItem(set) == expected

@pytest.mark.printing
def test_alignDotInCenter():
    assert PrintingCharts.alignDotInCenter(1) == PrintingCharts.blackDot()
    assert PrintingCharts.alignDotInCenter(2) == '_'+PrintingCharts.blackDot()
    assert PrintingCharts.alignDotInCenter(3) == '_' + PrintingCharts.blackDot() + '_'
    assert PrintingCharts.alignDotInCenter(4) == '__' + PrintingCharts.blackDot() + '_'
    assert PrintingCharts.alignDotInCenter(5) == '__' + PrintingCharts.blackDot() + '__'

@pytest.mark.printing
@pytest.mark.parametrize('set, expected, param', [
    (['apple', 'banana', 'cocoa', 'marakuija'], 'apple|banana|cocoa|marakuija', None),
    (['apple', 'banana', 'cocoa', 'marakuija'], 'apple | banana | cocoa | marakuija', ' | '),
    (['apple', 'banana', 1, 'marakuija'], 'apple / banana / 1 / marakuija', ' / '),
    (('apple', 'banana', 1, 'some', 'marakuija'), 'apple / banana / 1 / some / marakuija', ' / '),
])
def test_convertListToString(set, expected, param):
    if param is None:
        string = PrintingCharts.convertListToString(set)
    else:
        string = PrintingCharts.convertListToString(set, param)

    assert type(string) == str
    assert string == expected

def test_blackDot_Exception():
    # with pytest.raises(Exception):
        # blackDot('some string')
    pass

@pytest.mark.printing
@pytest.mark.parametrize('set1, set2, expect', [
    (1561.98, 10, 1560),
    (1564.18, 10, 1570),
    (1563.18, 10, 1560),
    (1563.18, 100, 1600),
    (1543.18, 100, 1600),
    (1533.18, 100, 1500),
    (1573.18, 50, 1600),
    (1563.18, 50, 1550),
    (1543.18, 50, 1550),
    (1533.18, 50, 1550),
    (1523.18, 50, 1550),
    (1520.18, 50, 1550),
    (1519.18, 50, 1500),
])
def test_roundValueForChart(set1, set2, expect):
    assert PrintingCharts.getRoundedValue(set1, set2) == expect

@pytest.mark.printing
@pytest.mark.parametrize('set1, set2, expect', [
    (123.061, 0.1, 123.1),
    (123.05, 0.1, 123.1),
    (123.041, 0.1, 123.1),
    (123.021, 0.1, 123.0),
    (123.005, 0.1, 123.0),
    
    (123.9, 0.5, 124.0),
    (123.718, 0.5, 124.0),
    (123.708, 0.5, 124.0),
    (123.618, 0.5, 123.5),
    (123.418, 0.5, 123.5),
    (123.25, 0.5, 123.5),
    (123.19, 0.5, 123.0),
    (123.061, 0.5, 123.0),
    (123.05, 0.5, 123.0),
    (123.041, 0.5, 123.0),
    (123.021, 0.5, 123.0),
    (123.005, 0.5, 123.0),

    (44.0038, 0.01, 44.0),
    (44.0041, 0.01, 44.01),
    (44.013, 0.01, 44.01),
    (44.021, 0.01, 44.02),
    (44.024, 0.01, 44.02),
    (44.025, 0.01, 44.03),
])
def test_roundLessThanOne(set1, set2, expect):
    result = PrintingCharts.getRoundedValue(set1, set2)
    assert result == expect

@pytest.mark.printing
@pytest.mark.parametrize('set, expect', [
    ('1231.456', 1231.456),
    ('1231,456', 1231.456),
    ('1231456', 1231456),
    ('1231uah', 1231),
    ('5231 грн', 5231),
    ('1231,456 грн', 1231.456),
    ('fsdfewf', 0),
    ('fsdfewf65', 65),
    ('15fs.dfe15wf', 15),
    ('fs.dfe015wf', 15),
    ('', 0)
])
def test_intOrFloatString(set, expect):
    assert PrintingBasic.intOrFloatString(set) == expect
