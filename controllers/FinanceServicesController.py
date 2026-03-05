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
        ratesHistory = bankProvider.returnCurrenciesRatesHistoryPrepared()

        print(ratesHistory)
        pass
