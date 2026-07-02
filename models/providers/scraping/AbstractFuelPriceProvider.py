import bs4
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup as BS
from models.providers.HttpProvider import HttpProvider

class AbstractFuelPriceProvider(ABC):

    soupObject: bs4.BeautifulSoup|bool

    fuel_brands = {
        # 'ДП':   {'s_type_': 'ДП', 's_brand_': 'Євро5'},
        # 'A95':  {'s_type_': '95', 's_brand_': 'Євро5-Е10'},
        # 'A95M': {'s_type_': '95', 's_brand_': 'Mustang Євро5-Е10'},
        # 'A100': {'s_type_': '100', 's_brand_': 'Mustang Євро5-Е0'}
    }

    url = ''

    def __init__(self) -> None:

        if not self.url:
            raise ValueError('Fuel Price Provider url must be defined (and be a valid url)')

        self.requestResult = self.fetchHtml(self.url)
        self.soupObject = self.makeSoupObject()

    def makeSoupObject(self):
        if self.soupObject is False:
            self.soupObject = BS(str(self.requestResult), 'html.parser')
        return self.soupObject

    def fetchHtml(self, url: str):
        self.requestResult = HttpProvider().getHtmlByUrl(url)
        return self.requestResult
    
    @abstractmethod
    def fetchTheFuelPrice(self) -> bool|float:
        pass
