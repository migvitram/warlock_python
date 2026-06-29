import os
import json

class JsonFiles:
        
    @staticmethod
    def writeToTheLocalJsonStorage(dataToWrite, fileName):

        jsonToFile = json.dumps(dataToWrite)
        jsonFile = open(fileName, '+w')
        result = jsonFile.write(jsonToFile)

        # print('storing result : ', result)

    @staticmethod
    def readDataFromJsonFile(fileName, mode='r') -> object:
        with open(fileName, mode) as file:
            return json.load(file)

    @staticmethod
    def updateDictionary(dictionary: dict, dataToAdd):
        for key, item in dataToAdd.items():
            # if
            pass

    @staticmethod
    def runSelfDiagnostics(storageFileName, default = {}):
        if not JsonFiles.checkFileExist(storageFileName):
            JsonFiles.initiateJsonStorageFile(storageFileName, defaultStructure=default)

    @staticmethod
    def checkFileExist(fileName: str) -> bool:
        return os.path.exists(fileName) and os.path.isfile(fileName)

    @staticmethod
    def initiateJsonStorageFile(fileName: str, defaultStructure = {}):
        fileName = os.path.abspath(fileName)
        try:
            file = open(fileName, 'w+')
            file.write(json.dumps(defaultStructure))
        except Exception as e:
            print('JsonFiles.py can not initiate json file.')
            print(e)
            return False
        return True

    @staticmethod
    def checkPropertyInDictAndCreateIfNotExist(dictionary: dict, propName: str, propValue: str=''):
        if propName not in dictionary:
            dictionary[propName] = propValue

    @staticmethod
    def defaultStructureOfJsonStorage() -> list:
        return [{'productName': '', 'url': '', 'presence': '', 'price': '', 'priceHistory': {}}]

    @staticmethod
    def deleteJsonFile(filePath: str):
        filePath = os.path.abspath(filePath)
        if JsonFiles.checkFileExist(filePath):
            os.remove(filePath)
            return True
        else:
            print(f"There is no file found : {filePath} !")
            return False