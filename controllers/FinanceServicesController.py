from models.providers.MonoBankApiProvider import MonoBankApiProvider
from models.helpers.Printing import Printing

class FinanceServices:

    def __init__(self) -> None:
        pass

    def retrieveDailyCurrenciesRate(self):
        # retrieve the data and store it
        bankProvider = MonoBankApiProvider()
        currenciesRates = bankProvider.getCurrencyRates()
        Printing.printDictionaryAsTable(currenciesRates)

    def printTheCurrenciesRateHistory(self):
        bankProvider = MonoBankApiProvider()
        # [MonoBankApiProvider.CURR_USD, MonoBankApiProvider.CURR_EUR]
        ratesHistory = bankProvider.returnCurrenciesRatesHistoryPrepared([MonoBankApiProvider.CURR_USD, MonoBankApiProvider.CURR_EUR])
        Printing.printDictionaryAsMultiChart('Currencies rates history', ratesHistory)
