import sys
import os
import pytest

sys.path.append(os.path.abspath('./..'))

from models.helpers.JsonFiles import JsonFiles

@pytest.mark.jfiles
@pytest.mark.parametrize('input, expected', [
    ('temp/some_file.json', False),
    ('temp/.gitignore', True),
    ('storage/some_json.file', False),
    ('storage/existed_empty_test_file.json', True),
])
def test_checkFileNotExist(input, expected):
    filePath = os.path.abspath(input)
    assert JsonFiles.checkFileExist(filePath) == expected

@pytest.mark.jfiles
@pytest.mark.parametrize('set, expected1, expected2, expected3', [
    ('test-file/path/file.json', False, False, False),
    ('storage/test_file.json', False, True, True),
    ('storage/existed_empty_test_file.json', True, True, True),
])
def test_jsonFilesCreatDeletion(set, expected1, expected2, expected3):
    filePath = os.path.abspath(set)
    assert os.path.exists(filePath) == expected1
    assert JsonFiles.initiateJsonStorageFile(set) == expected2
    assert JsonFiles.deleteJsonFile(set) == expected3
    if set == 'storage/existed_empty_test_file.json':
        JsonFiles.initiateJsonStorageFile(set)

@pytest.mark.jfiles
@pytest.mark.parametrize('set,expected1, expected2', [
    (None, True, {}),
    ({}, True, {}),
    ({'key1': 'value1', 'key2': ['some1', 'some2']}, True, {'key1': 'value1', 'key2': ['some1', 'some2']}),
])
def test_defaultStructureForJsonFiles(set, expected1, expected2):
    filePath = os.path.abspath('storage/default_structure_test_file.json')
    if set is None:
        assert JsonFiles.initiateJsonStorageFile(filePath) == expected1
    else:
        assert JsonFiles.initiateJsonStorageFile(filePath, set) == expected1
    assert JsonFiles.readDataFromJsonFile(filePath) == expected2
    os.remove(filePath)
