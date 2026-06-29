from models.providers.scraping.AbstractFuelPriceProvider import AbstractFuelPriceProvider

class WOGProvider(AbstractFuelPriceProvider):

    soupObject = False
    url = 'https://wog.ua/ua/fuels/'

    priceItemStructure = {
        's_fuel_list': {
            's_fuel_item_': {
                's_name_': {
                    's_type_': '',
                    's_brand_': '',
                },
                's_price_': {},
            }
        },
    }

    priceTag = 's_price_'

    requestResult = ''

    def checkAndStorePrices(self):
        for brand in self.fuel_brands:
            pass
        pass

    def fetchTheFuelPrice(self, brandText: str='Євро5') -> bool|float:
        tag = self.soupObject.find(
            lambda tag: tag.name == 'div'
            and any(css_class.startswith('s_brand_') for css_class in tag.get('class', []))
            and tag.get_text(strip=True) == brandText
        )

        fuel_item = tag.parent.parent

        fuel_price = fuel_item.find(
            lambda child: child.name == 'div'
            and any(css_class.startswith('s_price_') for css_class in child.get('class', []))
        )

        return float(fuel_price.get_text().strip()) if fuel_price is not None else False

    def fetchTheGasPrice(self):
        pass

    def fetchThePrices(self):
        pass

    def getBrands(self):
        return self.fuel_brands