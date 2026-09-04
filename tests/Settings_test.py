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

@pytest.mark.settings
@pytest.mark.parametrize('set, expect', [
    ('existedTestParam', True),
    ('nonExistentParam', False)
])
def test_paramExists(set, expect):
    filePath = 'storage/personal_settings.json'
    with open(filePath, 'w') as file:
        file.write(json.dumps({'existedTestParam': 'value'}))
    
    assert Settings.paramExists(set) == expect

    os.remove(filePath)

@pytest.mark.settings
@pytest.mark.parametrize('set1, set2, expect', [
    ('paramBool', True, True),
    ('paramNoneRaw', None, None),
    ('paramInt', 15514, 15514),
    ('paramString', 'some string', 'some string'),
    ('paramList', ['a', 'b', 'c'], ['a', 'b', 'c']),
    ('paramDict', {'key1': 'value1', 'key2': 123}, {'key1': 'value1', 'key2': 123}),
    ('paramTuple', ('a', 'b'), ['a', 'b']),
    ('paramListEmpty', [], []),
    ('paramDictEmpty', {}, {}),
    ('paramTuplEmpty', (), []),
])
def test_getStrict(set1, set2, expect):
    filePath = 'storage/personal_settings.json'
    with open(filePath, 'w') as file:
        file.write(json.dumps({set1: set2}))
    
    assert Settings.getStrict(set1) == expect
    assert Settings.getStrict('nonExistentParam') == None

    os.remove(filePath)