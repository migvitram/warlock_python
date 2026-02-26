import os
import json

class JsonFiles:
        
    @staticmethod
    def writeToTheLocalJsonStorage(dataToWrite, fileName):

        # dataToWrite = (
        #     {
        #         "url": "https://knigoland.com.ua/rozpovidi-pro-pilota-pirksa-6fx-item",
        #         "bookTitle": "Розповіді про пілота Піркса"
        #     },
        #     {
        #         "url": "https://knigoland.com.ua/povernennya-iz-zirok--item",
        #         "bookTitle": "Повернення з зірок"
        #     },
        #     {"url":"https://knigoland.com.ua/kiberiada-item", "bookTitle":"Кіберіада"},
        # )

        jsonToFile = json.dumps(dataToWrite)
        jsonFile = open(fileName, '+w')
        result = jsonFile.write(jsonToFile)

        # print('storing result : ', result)

    @staticmethod
    def readDataFromJsonFile(fileName, mode='r') -> list:
        with open(fileName, mode) as file:
            return json.load(file)

    @staticmethod
    def updateDictionary(dictionary: dict, dataToAdd):
        for key, item in dataToAdd.items():
            # if
            pass

    @staticmethod
    def runSelfDiagnostics(storageFileName):
        if not JsonFiles.checkFileExist(storageFileName):
            JsonFiles.initiateJsonStorageFile(storageFileName,
                JsonFiles.defaultStructureOfJsonStorage()
            )

    @staticmethod
    def checkFileExist(fileName: str) -> bool:
        return os.path.exists(fileName) and os.path.isfile(fileName)

    @staticmethod
    def initiateJsonStorageFile(fileName: str, defaultStructure):

        file = open(fileName, 'w+')
        file.write(json.dumps(defaultStructure))

        # print(json.load(open(os.path.abspath('storage/products_to_check.json'))))
        # file.write
        pass    

    @staticmethod
    def checkPropertyInDictAndCreateIfNotExist(dictionary: dict, propName: str, propType: str=''):
        if propName not in dictionary:
            dictionary[propName] = propType

    @staticmethod
    def defaultStructureOfJsonStorage() -> list:
        return [{'productName': '', 'url': '', 'presence': '', 'price': '', 'priceHistory': {}}]
