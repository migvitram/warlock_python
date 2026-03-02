import pytest
from models.helpers.SoupHelper import SoupHelper
from bs4 import BeautifulSoup as BS
import bs4

@pytest.mark.soup
@pytest.mark.parametrize('set, expect', [
    ('1 560', 1560),
    ('1&nbsp;564', 1564),
])
def test_trimNumberText(set, expect):
    assert SoupHelper.trimNumberText(set) == expect

@pytest.mark.soup
@pytest.mark.parametrize('set1, set2, expect', [
    ('<html><body><p class="random-css-class">Some text </p></body></html>', 'Some text', True),
    ('<html><body>'
    '<p class="random-css-class">'
    ' Some text '
    '</p>'
    '</body></html>', 'Some text', True),
    ('<html><body><p class="random-css-class">Some&nbsp;text</p></body></html>', 'Some text', True),
    ('<html><body><p class="random-css-class another-did">'
    'Some&nbsp;text'
    '</p></body></html>', 'Not some text', False),
])
def test_checkElementTextEquals(set1, set2, expect):
    soup = BS(set1, 'html.parser')
    findElement = soup.find('p', {'class': 'random-css-class'})
    assert isinstance(findElement, bs4.element.Tag) == True
    assert SoupHelper.checkElementTextEquals(findElement, set2) is expect
    
