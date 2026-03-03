import re
import bs4
from models.providers.scraping.AbstractScrapingProvider import AbstractScrapingProvider
from models.helpers.SoupHelper import SoupHelper
from models.helpers.Printing import Printing
from models.helpers.Logger import Logger

class Rozetka(AbstractScrapingProvider):

    domain = 'rozetka.com.ua'

    requestResult = ''
    
    def __init__(self) -> None:
        super().__init__()
        pass

    def fetchTheProductPrice(self):
        priceObject = self.findElementByCssClass('p', 'product-price__big')

        if isinstance(priceObject, bs4.element.Tag):
            text = priceObject.get_text()
            value = re.findall('(\\d+)', text)
            return ''.join(value)
        else:
            return False

    def fetchTheProductPresence(self):
        presenceObject = self.findElementByCssClass('p', 'status-label')
        presenceCheckResult = SoupHelper.checkElementTextEquals(presenceObject, 'Є в наявності')
        absenceCheckResult = SoupHelper.checkElementTextEquals(presenceObject, 'Немає в наявності')

        if presenceCheckResult == True and absenceCheckResult == True:
            Logger.log("Some shit : " + str(self.__class__) + ' with presence check' + presenceObject.get_text() + str(len(presenceObject.get_text())))

        if presenceCheckResult == False and absenceCheckResult == False:
            Printing.print("Something went wrong, or there is no product status on the page.")
            return False
        else:
            return 'Yes' if presenceCheckResult else 'No'
