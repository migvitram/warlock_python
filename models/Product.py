import os
from models.helpers.JsonFiles import JsonFiles

class Product:

    jsonProductStorage = os.path.abspath('storage/products_to_check.json')

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"Product(name={self.name}, price={self.price})"
    
    @staticmethod
    def getProductDetailsByName(productName: str) -> dict:
        productsSet = JsonFiles.readDataFromJsonFile(Product.jsonProductStorage)
        for product in productsSet:
            if productName.lower() in (product['productName']).lower():
                details = [
                    {'parameter': 'productName', 'value': product['productName']},
                    {'parameter': 'url', 'value': product['url']},
                    {'parameter': 'price', 'value': product['price']},
                    {'parameter': 'presence', 'value': product['presence']},
                    {'parameter': 'date', 'value': product['date']},
                ]
                return details
        return {}

    @staticmethod
    def getProductsPriceHistoryByName(productName: str) -> dict:
        products = {}
        productsSet = JsonFiles.readDataFromJsonFile(Product.jsonProductStorage)
        dataIntegrity = {'setLength': 0, 'errors': 0, 'integrity': True, 'bigest': []}

        for product in productsSet:
            if productName.lower() in (product['productName']).lower():
                newProduct = product['priceHistory'] if 'priceHistory' in product else []
                if dataIntegrity['setLength'] < len(newProduct):
                    dataIntegrity['setLength'] = len(newProduct)
                    dataIntegrity['bigest'] = newProduct

                # dataIntegrity['setLength'] = len(newProduct) if len(newProduct) > dataIntegrity['setLength'] else dataIntegrity['setLength']
                products[product['productName']] = newProduct

        for productName, priceHistory in products.items():
            if len(priceHistory) < dataIntegrity['setLength']:
                etalonHistory = dataIntegrity['bigest']

                recoveredDict = {}
                for point, value in etalonHistory.items():
                    if point not in priceHistory.keys():
                        recoveredDict[point] = 0
                    else:
                        recoveredDict[point] = priceHistory[point]
                
                products[productName] = recoveredDict

        return products