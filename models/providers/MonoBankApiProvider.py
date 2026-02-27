import requests
from datetime import datetime
from models.helpers.JsonFiles import JsonFiles

class MonoBankApiProvider:

    bankApiUrl = 'https://api.monobank.ua/'
    bankCurrRateApiUrl = 'https://api.monobank.ua/bank/currency'

    CURR_UAH = '980'
    CURR_USD = '840'
    CURR_EUR = '978'
    CURR_GBP = '826'

    def __init__(self) -> None:
        pass

    def retreiveApiData(self):
        return requests.get(MonoBankApiProvider.bankCurrRateApiUrl).json()

    def getCurrencyRates(self):
        # data = self.retreiveApiData()
        data = JsonFiles.readDataFromJsonFile('storage/currencies_rates.json')
        # choose the currencies to store
        # self.storeCurrenciesRatesToHistory([])
        preparedData = []
        for row in data[0:4]:
            newRow = {}
            for paramName, param in self.currRateResponseStructure().items():
                if paramName in row.keys():
                    if 'method' in param:
                        if hasattr(self, param['method']):
                            newRow[param['name']] = getattr(self, param['method'])(row[paramName])
                    else:
                        newRow[param['name']] = row[paramName]
                else:
                    newRow[param['name']] = ''
            preparedData.append(newRow)
        return preparedData

    def storeCurrenciesRatesToHistory(self, data):

        pass

    def getCurrencyName(self, currCode: str=''):
        currNames = {
                self.CURR_EUR: 'Euro', 
                self.CURR_USD: 'Dollar', 
                self.CURR_UAH: 'Гривня',
                self.CURR_GBP: 'British Pound sterling'
            }
        return currNames[str(currCode)] if str(currCode) in currNames.keys() else 'unknown'

    def currRateResponseStructure(self):
        return {
            'currencyCodeA': {'type': int, 'required': True, 'name': 'from', 'method': 'convertCurrName'},
            'currencyCodeB': {'type': int, 'required': True, 'name': 'to', 'method': 'convertCurrName'},
            'date': {'type': int, 'required': True, 'name': 'date', 'method': 'convertDate'},
            'rateBuy': {'type': float,'required': False, 'name': 'Buying rate'},
            'rateSell': {'type': float,'required': False, 'name': 'Selling rate'},
            'rateCross': {'type': float,'required': False, 'name': 'Cross rate'}
        }

    def convertCurrName(self, data):
        return self.getCurrencyName(data)

    def convertDate(self, data):
        return datetime.fromtimestamp(data)
