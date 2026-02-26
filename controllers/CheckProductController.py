import sys
import os
import time
import urllib.request
sys.path.append(os.path.abspath('./..'))

from models.helpers.SoupHelper import SoupHelper
from models.helpers.Printing import Printing
from models.helpers.JsonFiles import JsonFiles
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

        def getHtmlData(url):
            return urllib.request.urlopen(url)

        for item in booksSet:
            rawHtml = urllib.request.urlopen(item['url'])
            html = rawHtml.read().decode('utf-8')
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
        for product in storedData[:]:
            if product['productName'] == productToDeleteName:
                storedData.remove(product)
        JsonFiles.writeToTheLocalJsonStorage(storedData, self.jsonFileStorage)
        pass

    def printTheSummaryProductTable(self):
        storedData = JsonFiles.readDataFromJsonFile(self.jsonFileStorage)
        Printing.printDictionaryAsTable(storedData, ['productName', 'url', 'price', 'presence', 'date'])

    def printTheProductPriceChart(self, productId):
        productsSet = JsonFiles.readDataFromJsonFile(self.jsonFileStorage)
        if 'priceHistory' in productsSet[productId]:
            Printing.printDictionaryAsChart("Price changes for last 5 days", productsSet[productId]['priceHistory'], showOnlyDotValues=False)
        else:
            print("There is no Price History for this product yet! \n")
