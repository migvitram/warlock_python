import os
import json
import pytest
from models.PersonalSettings import Settings

@pytest.mark.settings
def test_checkSettingStorage():
    filePath = 'storage/personal_settings.json'
    assert os.path.exists(filePath) == False

    Settings.checkSettingStorage()
    assert os.path.exists(filePath) == True

    os.remove(filePath)

@pytest.mark.settings
@pytest.mark.parametrize('set, expect', [
    ('string', 'string'),
    (15648, 15648),
    (['a', 'b', 154], ['a', 'b', 154]),
    ({'a': 'string', 'b': 65165165, 'c': ['e', 'f', 'g']}, {'a': 'string', 'b': 65165165, 'c': ['e', 'f', 'g']})
])
def test_setParam(set, expect):
    filePath = 'storage/personal_settings.json'
    
    Settings.updateParam('paramName', set)

    with open(filePath, 'r') as file:
        content = json.load(file)
        assert content['paramName'] == expect

    assert Settings.getParam("paramName") == expect

    os.remove(filePath)

@pytest.mark.settings
@pytest.mark.parametrize('set, expect', [
    ('string', 1),
    ('', 0),
    (23, 23),
    (True, 1),
    (False, 0),
    ([], 0),
    ({}, 0),
    ((), 0),
    (['a', 'b'], 1),
    (('a', 'b'), 1),
    ({'a': 65465}, 1)
])
def test_getAsInt(set, expect):
    filePath = 'storage/personal_settings.json'
    with open(filePath, 'w') as file:
        file.write(json.dumps({'paramName': set}))
    
    assert Settings.getAsInt('paramName') == expect
    os.remove(filePath)