import sys
import os
import pytest

sys.path.append(os.path.abspath('./..'))

from models.helpers.JsonFiles import JsonFiles

@pytest.mark.jfiles
@pytest.mark.parametrize('input, expected', [
    ('./temp/some_file.json', False),
    ('./some_json.file', False),
])
def test_checkFileNotExist(input, expected):
    filePath = os.path.abspath(input)
    assert JsonFiles.checkFileExist(filePath) == expected

