import bs4
import re
from models.providers.scraping.AbstractScrapingProvider import AbstractScrapingProvider

class KnigarniaYe(AbstractScrapingProvider):

    domain = 'book-ye.com.ua'

    def __init__(self) -> None:
        super().__init__()
        pass

    def visitThePage(self, url: str):
        self.requestResult = self.fetchHtml(url)
        self.makeSoupObject()
        self.productPresence = self.fetchTheProductPresence()
        self.productPrice = self.fetchTheProductPrice()
        return True
    
    def fetchTheProductPrice(self):
        priceObject = super().findElementByCssClass('span', 'price')

        if isinstance(priceObject, bs4.element.Tag):
            text = priceObject.get_text()
            value = re.findall('\d+', text)
            return value[0] if len(value) > 0 else False
        else:
            return False

    def fetchTheProductPresence(self):
        presenceContainer = self.findElementByCssClass('div', 'availability')
        print(type(presenceContainer), type(presenceContainer['data-value']))
        return 'Yes' if str(presenceContainer['data-value']) == '1' else "No"

    def returnProductPrice(self):
        return self.productPrice
    
    def returnProductPresence(self):
        return self.productPresence
