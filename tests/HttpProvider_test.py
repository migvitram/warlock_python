import pytest
import os
import sys
sys.path.append(os.path.abspath('./..'))

from models.providers.HttpProvider import HttpProvider

@pytest.mark.httpProvider
@pytest.mark.parametrize('set, expected', [
    ('', False),
    ('bqfasfwefew', False),
    ('sodfij@dif.dod', False),
    ('ftp://some.dif.dod', True),
    ('http://some.dif.dod', True),
    ('http://some.dif.dod?foiwj=3fi3', True),
    ('https://sodfij@dif.dod', False),
    ('https://sodfij.dif.cod', True),
    ('https://sodfij.dif.dod?difj=23f9f&sfio2=asdfef', True),
])
def test_isHyperLink(set, expected):
    assert HttpProvider.isHyperlink(set) == expected