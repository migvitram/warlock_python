import bs4
import re
from models.providers.scraping.AbstractScrapingProvider import AbstractScrapingProvider

class KnigarniaYe(AbstractScrapingProvider):

    domain = 'book-ye.com.ua'

    def __init__(self) -> None:
        super().__init__()
        pass

    def fetchTheProductPrice(self):
        priceObject = super().findElementByCssClass('span', 'price')

        if isinstance(priceObject, bs4.element.Tag):
            text = priceObject.get_text()
            value = re.findall(r"\d+", text)
            return value[0] if len(value) > 0 else False
        else:
            return False

    def fetchTheProductPresence(self):
        presenceContainer = self.findElementByCssClass('div', 'availability')
        return 'Yes' if str(presenceContainer['data-value']) == '1' else "No"
