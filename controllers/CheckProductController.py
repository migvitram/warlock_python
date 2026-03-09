import os
import time

from datetime import datetime
from libraries.printing.PrintingColor import Color
from models.helpers.Logger import Logger
from models.helpers.Printing import Printing
from models.helpers.JsonFiles import JsonFiles
from models.providers.HttpProvider import HttpProvider
from models.providers.scraping.AbstractScrapingProvider import AbstractScrapingProvider
from models.providers.scraping.KnigarniaYeProvider import KnigarniaYe
from models.providers.scraping.KnigolandProvider import Knigoland
from models.providers.scraping.RozetkaProvider import Rozetka

class CheckProductController:

    jsonFileStorage = ''
    
    providers: dict[str, type[AbstractScrapingProvider]]

    def __init__(self, storageFile: str) -> None:
        self.jsonFileStorage = os.path.abspath(storageFile)
        JsonFiles.runSelfDiagnostics(self.jsonFileStorage)
        self.providers = {
            'knigoland.com.ua': Knigoland, 
            'book-ye.com.ua': KnigarniaYe,
            'rozetka.com.ua': Rozetka
        }
        pass

    def chooseTheScrapingProvider(self, url: str) -> AbstractScrapingProvider|bool:
        domain = HttpProvider.getDomainFromUrl(url)
        if domain in self.providers.keys():
            return self.providers[HttpProvider.getDomainFromUrl(url)]()
        else:
            return False

    def runTheTracking(self):
        Logger.log("The prouct tracking fetch initiated ("+str(self.__class__)+")")
        print("Running the tracking...")
        time.sleep(1)
        print("this is the processor to parse the data from web-sites...")

        # according to the root directory (warlock)
        jsonFileStorage = self.jsonFileStorage

        productsSet = JsonFiles.readDataFromJsonFile(jsonFileStorage)

        print("Retrieving ... ")

        for item in productsSet:

            if HttpProvider.isHyperlink(item['url']):
                scrapProvider = self.chooseTheScrapingProvider(item['url'])
                if scrapProvider is not False:
                    today = datetime.now()
                    scrapProvider.visitThePage(item['url'])
                    price = scrapProvider.returnTheProductPrice()
                    item['presence'] = scrapProvider.returnTheProductPresence()
                    item['price'] = price
                    item['date'] = today.strftime("%d/%m/%Y, %H:%M:%S")
                    if 'priceHistory' not in item:
                        item['priceHistory'] = {}
                    item['priceHistory'][today.strftime("%d/%m/%Y")] = price
                else:
                    Printing.print("Can not find the scraping provider for product \'"+item['productName']+"\'", Color.YELLOW)

        Printing.printDictionaryAsTable(productsSet, ['url', 'productName', 'presence', 'price', 'date'])

        # write the new price data
        JsonFiles.writeToTheLocalJsonStorage(productsSet, jsonFileStorage)

    def addProductForTracking(self, productName: str, url: str):
        storedData = JsonFiles.readDataFromJsonFile(self.jsonFileStorage)
        storedData.append({'productName': productName, 'url': url, 'price': '0', 'presence': 'No'})
        JsonFiles.writeToTheLocalJsonStorage(storedData, self.jsonFileStorage)
        pass
    
    def removeProductByName(self, productToDeleteName: str):
        storedData = JsonFiles.readDataFromJsonFile(self.jsonFileStorage)
        result = False
        for product in storedData[:]:
            if product['productName'] == productToDeleteName:
                storedData.remove(product)
                JsonFiles.writeToTheLocalJsonStorage(storedData, self.jsonFileStorage)
                result = True
                break
            else:
                result = False
        if result == False:
            Printing.print("Can not find product \'"+productToDeleteName+"\' ", Color.RED)

    def printTheSummaryProductTable(self):
        storedData = JsonFiles.readDataFromJsonFile(self.jsonFileStorage)
        Printing.printDictionaryAsTable(storedData, ['productName', 'url', 'price', 'presence', 'date'])

    def printTheProductPriceChart(self, productName: str):

        productsSet = JsonFiles.readDataFromJsonFile(self.jsonFileStorage)
        productId = False
        for product in productsSet:
            if product['productName'] == productName:
                productId = productsSet.index(product)
                break

        if productId is False:
            Printing.print("There is no Price History for product named \'"+productName+"\'!", Color.RED)
            return

        if 'priceHistory' in productsSet[productId]:
            Printing.printDictionaryAsChart("Price changes for product \'"+productName+"\' for last 5 days", productsSet[productId]['priceHistory'], showOnlyDotValues=False)
        else:
            Printing.print("There is no Price History for this product yet! \n", Color.YELLOW)
        return

    def printDemo(self):
        testDict = {'22/05': 153, '12/06': 152, '14/07': 150, '25/08': 148, '14/09': 149, '05/10': 151,
            '18/11': 155, '02/12': 161, '23/01': 157, '23/02': 164}
        Printing.printDictionaryAsChart("DEMO History diagram (for single data set)", testDict)
        return

    def printDemoMulti(self):
        testDict = [
            {'22/05/2025': 153, '12/06/2025': 152, '14/07/2025': 150, '25/08/2025': 148, '14/09/2025': 147, '05/10/2025': 151,
            '18/11/2025': 155, '02/12/2025': 161, '23/01/2026': 157, '23/02/2026': 163, '20/03/2026': 164, '12/04/2026': 163, '3/05/2026': 160, '14/06/2026': 163},
            {'22/05/2025': 154, '12/06/2025': 156, '14/07/2025': 158, '25/08/2025': 159, '14/09/2025': 160, '05/10/2025': 162,
            '18/11/2025': 161, '02/12/2025': 162, '23/01/2026': 165, '23/02/2026': 163, '20/03/2026': 161, '12/04/2026': 160, '3/05/2026': 158, '14/06/2026': 157},
            {'22/05/2025': 144, '12/06/2025': 145, '14/07/2025': 146, '25/08/2025': 148, '14/09/2025': 150, '05/10/2025': 153,
            '18/11/2025': 155, '02/12/2025': 158, '23/01/2026': 162, '23/02/2026': 166, '20/03/2026': 164, '12/04/2026': 160, '3/05/2026': 161, '14/06/2026': 160}
        ]
        Printing.printDictionaryAsMultiChart("DEMO Multi History diagram (for multi data set)", testDict)
        return

    def printDemoTable(self):
        demoData = [
            {'productName': 'Product 1', 'url': 'http://some.url/for/product-1', 'price': 155, 'presence': 'Yes', 'date': '12/03/2026'},
            {'productName': 'Another test Product for table', 'url': 'http://some.url/for/another-product', 'price': 1628.00, 'presence': 'No', 'date': '10/02/2025'},
            {'productName': 'Test product 3', 'url': 'http://some.url/for/another-one test-product-3', 'price': 628.00, 'presence': 'Yes', 'date': '8/08/2025'},
        ]
        Printing.printDictionaryAsTable(demoData, ['productName', 'url', 'price', 'presence', 'date'])
        pass
