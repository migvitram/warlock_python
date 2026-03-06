from models.providers.MonoBankApiProvider import MonoBankApiProvider
from models.helpers.Printing import Printing
from models.helpers.Logger import Logger

class FinanceServices:

    def __init__(self) -> None:
        pass

    def retrieveDailyCurrenciesRate(self):
        Logger.log("The currencies rates fetch initiated ("+str(self.__class__)+")")
        # retrieve the data and store it
        bankProvider = MonoBankApiProvider()
        currenciesRates = bankProvider.getCurrencyRates()
        Printing.printDictionaryAsTable(currenciesRates)

    def printTheCurrenciesRateHistory(self):
        bankProvider = MonoBankApiProvider()
        ratesHistory = bankProvider.returnCurrenciesRatesHistoryPrepared([MonoBankApiProvider.CURR_USD, MonoBankApiProvider.CURR_EUR])
        Printing.printDictionaryAsMultiChart('Currencies rates history', ratesHistory)

    def printTheCurrencyRateHistory(self, currencyName: str):
        bankProvider = MonoBankApiProvider()
        ratesHistory = bankProvider.returnCurrencyRateHistoryPrepared(currencyName)
        Printing.printDictionaryAsChart('Currency '+currencyName.upper()+' rates history', ratesHistory, showOnlyDotValues=False)
