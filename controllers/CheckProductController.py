import sys
import os
import time
# sys.path.append(os.path.abspath('./..'))

from models.helpers.SoupHelper import SoupHelper
from models.helpers.Printing import Printing
from models.helpers.JsonFiles import JsonFiles
from models.providers.HttpProvider import HttpProvider
from bs4 import BeautifulSoup as BS
from datetime import datetime

class CheckProductController:

    jsonFileStorage = ''
    providers = ['Shop1.py', 'Shop2.py']

    def __init__(self, storageFile: str) -> None:
        self.jsonFileStorage = os.path.abspath(storageFile)
        JsonFiles.runSelfDiagnostics(self.jsonFileStorage)
        pass

    def run(self):

        print("Running the tracking...")
        print("\n")
        time.sleep(1)
        print("this is the processor to parse the data from web-sites...")
        print("\n")

        # according to the root directory (warlock)
        jsonFileStorage = self.jsonFileStorage

        booksSet = JsonFiles.readDataFromJsonFile(jsonFileStorage)

        print("Retrieving ... ")
        print("\n")

        for item in booksSet:
            html = HttpProvider.getHtmlByUrl(item['url'])
            today = datetime.now()
            price = SoupHelper.checkThePrice(html)
            item['presence'] = SoupHelper.checkTheProduct(html)
            item['price'] = price
            item['date'] = today.strftime("%d/%m/%Y, %H:%M:%S")
            if 'priceHistory' not in item:
                item['priceHistory'] = {}
            item['priceHistory'][today.strftime("%d/%m/%Y")] = price

        Printing.printDictionaryAsTable(booksSet, ['url', 'productName', 'presence', 'price', 'date'])

        # write the new price data
        JsonFiles.writeToTheLocalJsonStorage(booksSet, jsonFileStorage)

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
            Printing.print("Can not find product \'"+productToDeleteName+"\' ", Printing.RED)

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
            Printing.print("There is no Price History for product named \'"+productName+"\'!", Printing.RED)
            return

        if 'priceHistory' in productsSet[productId]:
            Printing.printDictionaryAsChart("Price changes for last 5 days", productsSet[productId]['priceHistory'], showOnlyDotValues=False)
        else:
            print("There is no Price History for this product yet! \n")
        return

    def printDemo(self):
        testDict = {'22/05': 153, '12/06': 152, '14/07': 150, '25/08': 148, '14/09': 149, '05/10': 151,
            '18/11': 155, '02/12': 161, '23/01': 157, '23/02': 164}
        Printing.printDictionaryAsChart("DEMO History diagram (for single data set)", testDict)
        return

    def printDemoTable(self):
        demoData = [
            {'productName': 'Product 1', 'url': 'http://some.url/for/product-1', 'price': 155, 'presence': 'Yes', 'date': '12/03/2026'},
            {'productName': 'Another test Product for table', 'url': 'http://some.url/for/another-product', 'price': 1628.00, 'presence': 'No', 'date': '10/02/2025'},
            {'productName': 'Test product 3', 'url': 'http://some.url/for/another-one test-product-3', 'price': 628.00, 'presence': 'Yes', 'date': '8/08/2025'},
        ]
        Printing.printDictionaryAsTable(demoData, ['productName', 'url', 'price', 'presence', 'date'])
        pass
