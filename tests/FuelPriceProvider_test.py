import pytest
import os
import sys
sys.path.append(os.path.abspath('./..'))

from models.providers.scraping.WOGProvider import WOGProvider

@pytest.mark.fuelPrice
def test_wogGetBrands():
    prov = WOGProvider()
    result = prov.getBrands()
    assert isinstance(result, dict) == True
    assert 'ДП' in result
