from models.providers.scraping.AbstractScrapingProvider import AbstractScrapingProvider
from models.helpers.SoupHelper import SoupHelper

class ShopATB(AbstractScrapingProvider):

    domain = 'www.atbmarket.com'

    # https://www.atbmarket.com/catalog/economy?page=2
    economy = 'https://www.atbmarket.com/catalog/economy'

    def __init__(self) -> None:
        super().__init__()
        pass

    def fetchTheProductPrice(self):
        priceGrnObject = super().findElementByCssPath('.product-price__top > span')
        priceCoinsObject = super().findElementByCssClass('span', 'product-price__coin')

        if priceGrnObject is not None:
            if priceCoinsObject is not None:
                return round((float)(priceGrnObject.get_text().strip()), 2)
            return round((float)(priceGrnObject.get_text().strip() + '.00'), 2)
        else:
            return False

    def fetchTheProductPresence(self):
        presenceContainer = self.findElementByCssClass('span', 'available-tag__text')
        presenceCheckResult = SoupHelper.checkElementTextEquals(presenceContainer, 'Є в наявності')
        
        return 'Yes' if presenceCheckResult else "No"