import sys
import os
import pytest
sys.path.append(os.path.abspath('./..'))
import abilities

@pytest.mark.abilities
@pytest.mark.parametrize('set, expected', [
    ('Please', True),
    ('please', True),
    ('please,', True),
    ('Please,', True),
    ('damn', True),
    ('shit', True),
    ('run', False),
    ('the', False),
    ('file', False),
    ('search', False),
    ('spider', False),
])
def test_wrongWords(set, expected):
    assert abilities.wrongWord(set) == expected

@pytest.mark.abilities
@pytest.mark.parametrize('set, expected', [
    ('Yes', False),
    ('No, thank you', True),
    ('exit', True),
    ('exit,', True),
    ('No, exit', True),
    ('No', True),
    ('no', True),
    ('run', False),
    ('the', False),
    ('file', False),
    ('search', False),
    ('spider', False),
])
def test_checkWishmasterSatisfied(set, expected):
    assert abilities.checkWishmasterSatisfied(set) == expected


def test_filter():
    sentence = ['some', 'please', 'word', 'run', 'shit', 'spider']
    result = filter(abilities.correctWord, sentence)
    assert list(result) == ['some', 'word', 'run', 'spider']
