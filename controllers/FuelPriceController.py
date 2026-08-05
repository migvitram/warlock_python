import os
import traceback
from datetime import datetime
from models.providers.scraping.WOGProvider import WOGProvider
from models.helpers.JsonFiles import JsonFiles
from models.helpers.Logger import Logger
from models.helpers.Printing import Printing

class FuelPriceController:

    jsonFileStorage = ''
    providers = []

    def __init__(self) -> None:
        storageFile = 'storage/fuel_prices_history.json'
        self.jsonFileStorage = os.path.abspath(storageFile)
        JsonFiles.runSelfDiagnostics(self.jsonFileStorage)
        providers = {'WOG': WOGProvider}

    def checkPrices(self, salesCompany: str='WOG'):

        pricesSet = JsonFiles.readDataFromJsonFile(self.jsonFileStorage)
        prov = WOGProvider()

        today = datetime.now().strftime("%d/%m/%Y")
        brands = prov.getBrands()
        result = []
        
        for brand in brands.keys():
            brandName = brands[brand]['s_brand_']
            if brand not in pricesSet:
                pricesSet[brand] = {'priceHistory': {}}
            
            try:
                price = prov.fetchTheFuelPrice(brandName)
                pass
            except Exception as e:
                Printing.print(f"Error during one of the fuel price tracking. Check app.log file to see more")
                Logger.log(f"Error : {e}" + "\n" + traceback.format_exc())
                price = None

            pricesSet[brand]['priceHistory'][today] = price
            result.append({'brand': brand, 'price': price, 'date': today})

        JsonFiles.writeToTheLocalJsonStorage(pricesSet, self.jsonFileStorage)
        Printing.printDictionaryAsTable(result)

    def printPriceHistory(self):
        storedData = JsonFiles.readDataFromJsonFile(self.jsonFileStorage)
        preparedData = {}
        for brandName, brandData in storedData.items():
            preparedData[brandName] = brandData['priceHistory']
        Printing.printDictionaryAsMultiChart('Fuel prices history', preparedData, step=0.5)

    def printBrandPriceHistory(self, fuelBrand: str):
        storedData = JsonFiles.readDataFromJsonFile(self.jsonFileStorage)
        preparedData = {}
        for brandName, brandData in storedData.items():
            if brandName == fuelBrand:
                preparedData = brandData['priceHistory']
        Printing.printDictionaryAsChart('Fuel prices history for brand '+fuelBrand, preparedData, showOnlyDotValues=False, step=0.5)
