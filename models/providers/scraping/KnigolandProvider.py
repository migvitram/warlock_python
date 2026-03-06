import bs4
import re
from models.providers.scraping.AbstractScrapingProvider import AbstractScrapingProvider
from models.helpers.Logger import Logger

class Knigoland(AbstractScrapingProvider):

    domain = 'knigoland.com.ua'
    requestResult = ''
    
    def __init__(self) -> None:
        super().__init__()
        pass

    def fetchTheProductPrice(self):
        priceObject = self.findElementByCssClass('div', 'price')

        if isinstance(priceObject, bs4.element.Tag):
            text = priceObject.get_text()
            value = re.findall(r"(\d+)", text)
            return value[0] if len(value) > 0 else False
        else:
            return False

    def fetchTheProductPresence(self):
        presenceCheckResult = super().checkElementPresentByText('В наявності', 'span')
        absenceCheckResult = super().checkElementPresentByText('Немає в наявності', 'span')

        if presenceCheckResult == False and absenceCheckResult == False:
            print("something went wrong, or there is no product status on the page")
            Logger.log("Did not find the element (in "+self.__class__.__name__+")")
            return False
        else:
            return 'Yes' if presenceCheckResult else 'No'
