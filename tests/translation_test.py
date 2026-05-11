import pytest
from monadas.translation import _

@pytest.mark.translation
@pytest.mark.parametrize('set, expect', [
    ('', ''),
    ('text without translation', 'text without translation'),
    ('default translation with {param}', 'default translation with {param}'),
])
def test_default_translations(set, expect):
    assert _('app', set) == expect

@pytest.mark.translation
@pytest.mark.parametrize('set1, set2, expect', [
    ('default translation with {param}', {'param': 'VALUE'}, 'default translation with VALUE'),
])
def test_default_translation_with_params(set1, set2, expect):
    assert _('app', set1, set2) == expect

@pytest.mark.translation
@pytest.mark.parametrize('set1, set2, set3, expect', [
    ("Price changes for product '{productName}' for last {n} days", {}, None, "Price changes for product '{productName}' for last {n} days"),
    ("Price changes for product '{productName}' for last {n} days", {}, 'ua', "Зміни ціни продукту '{productName}' за минулі {n} днів"),
    ("Price changes for product '{productName}' for last {n} days", {'productName': 'Any Product'}, 'ua', "Зміни ціни продукту 'Any Product' за минулі {n} днів"),
    ("Price changes for product '{productName}' for last {n} days", {'productName': 'Some Another Product', 'n': 5}, 'ua', "Зміни ціни продукту 'Some Another Product' за минулі 5 днів"),
])
def test_default_translation_with_lang(set1, set2, set3, expect):
    assert _('app', set1, set2, set3) == expect