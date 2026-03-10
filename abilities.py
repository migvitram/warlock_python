import os
from controllers.CheckProductController import CheckProductController
from controllers.FinanceServicesController import FinanceServices
from models.helpers.Logger import Logger
from models.helpers.Printing import Printing
from libraries.printing.PrintingColor import Color
from datetime import datetime
from dotenv import load_dotenv
from monadas.translation import _
from models.AppContext import AppContext

load_dotenv()

def checkWishmasterSatisfied(want: str) -> bool:
    sentence = list(filter(correctWord, str.split(want.lower())))
    if ('no' in sentence) or 'no,' in sentence or ('exit' in sentence) or ('exit,' in sentence):
        return True
    return False

def checkTheWish(theWishText: str):
    lang = str(AppContext.get('lang'))

    # split the wish to the words
    jsonProductStoragePass = 'storage/products_to_check.json'
    sentence = str.split(theWishText)
    checkProduct = CheckProductController(jsonProductStoragePass)

    if len(sentence) > 1:

        iterator = filter(correctWord, sentence)
        sentence = list(iterator)

        if sentence[0] == 'clean' or sentence[0] == 'clear' or sentence[0] == 'purge':
            if sentence[1] == 'log':
                deleted = Logger.clean()
                if deleted:
                    Printing.print('Log file removed successfuly.', Color.GREEN)

        if sentence[0] == 'make':
            if sentence[1] == 'tests' or sentence[1] == 'self-tests':
                resultStatus = os.system('cd ./tests && pytest')

        if sentence[0] == 'run':
            if sentence[1] == 'the':
                if sentence[2] == 'product':
                    if sentence[3] == 'tracking':
                        checkProduct.runTheTracking()

        if sentence[0] == 'print':
            if sentence[1] == 'demo':
                checkProduct.printDemo()
                pass
            if sentence[1] == 'demo-multi':
                checkProduct.printDemoMulti()
                pass
            if len(sentence) > 2 and sentence[1] == 'demo' and sentence[2] == 'table':
                checkProduct.printDemoTable()
                pass
            
            if sentence[1] == 'the':
                if sentence[2] == 'product' and sentence[3] == 'price' and sentence[4] == 'history':
                    productName = askUntilAnswer(_('app', 'For what product?', lang)+" \n")
                    checkProduct.printTheProductPriceChart(productName)

                if sentence[2] == 'summary' and sentence[3] == 'product' and sentence[4] == 'table':
                    checkProduct.printTheSummaryProductTable()

                if sentence[2] == 'product' and sentence[3] == 'summary' and sentence[4] == 'table':
                    checkProduct.printTheSummaryProductTable()

                if sentence[2] == 'currencies' and sentence[3] == 'rate' and sentence[4] == 'history':
                    financeService = FinanceServices()
                    financeService.printTheCurrenciesRateHistory()
                    pass
                if sentence[2] == 'currency' and sentence[3] == 'rate' and sentence[4] == 'history' and sentence[5] == 'for':
                    financeService = FinanceServices()
                    if len(sentence) > 5 and sentence[6] != '':
                        financeService.printTheCurrencyRateHistory(sentence[6])
                        pass
                    if len(sentence) == 5:
                        currencyName = askUntilAnswer('Please, enter the currency short name (usd, eur, bps) : ')
                        financeService.printTheCurrencyRateHistory(currencyName)
                    pass

        if sentence[0] == 'add':
            if sentence[1] == 'the':
                if sentence[2] == 'product' and sentence[3] == 'for' and sentence[4] == 'tracking':
                    productName = askUntilAnswer(_('app', "Please, enter the product name!", lang)+" \n")
                    productUrl = askUntilAnswer(_('app', "Please, enter the product URL!", lang)+" \n")
                    checkProduct.addProductForTracking(productName, productUrl)
                    pass

        if sentence[0] == 'get':
            if sentence[1] == 'the':
                if sentence[2] == 'currencies' and sentence[3] == 'rates':
                    financeService = FinanceServices()
                    financeService.retrieveDailyCurrenciesRate()
                    pass

        if sentence[0] == 'remove' or sentence[0] == 'delete':
            if sentence[1] == 'the':
                if sentence[2] == 'product' and sentence[3] == 'for' and sentence[4] == 'tracking':
                    productName = askUntilAnswer(_('app', "Please, enter the name of the product you want to REMOVE!", lang)+" \n")
                    areYouSure = input("Are you sure, you want to delete product \""+productName+"\" from trackin? \n")
                    if areYouSure.lower() == 'yes' or areYouSure.lower() == 'y':
                        checkProduct.removeProductByName(productName)
                    else:
                        areYouSure = askUntilAnswer(_('app', "Please, enter \'yes\' or \'no\', or \'y\' or \'n\'", lang)+" \n")
                        if areYouSure.lower() == 'yes' or areYouSure.lower() == 'y':
                            checkProduct.removeProductByName(productName)

        if sentence[0] == 'change' and sentence[1] == 'the' and sentence[2] == 'language':
            lang = askUntilAnswer("please type the language short code [ua, ru, en] : ")
            if lang != '':
                AppContext.set('lang', lang)
        for word in sentence:
            # print(word)
            pass

        # to see the construction to_verb -> the_noun
        # if sentence has one or more consturctions -> try to execute (set to the queue)

        # print('args type', type(sentence))
        # print(sentence)

        if sentence[0] == 'exit':
            Printing.print("Glory to you, Wishmaster! \n", Color.GREEN)
            return exit
    else:
        Printing.print("Please, clearify you wish, Wishmaster!", Color.YELLOW)
    return

def askUntilAnswer(question: str) -> str:
    param = ''
    while param == '':
        param = input(question)
    return param

# List of abbilities
# to run the file, to write the text, to check the text by hyperlink and check some word/data
# to search the specified data among text/news
def knownComands() -> dict:
    return {
        'run': {
            'spider': {
                'file': 'controllers/run.py'
            }
        }, 
        'write': [], 
        'check': [], 
        'find': []
    }

def correctWord(word: str):
    return not wrongWord(word)

def wrongWord(word: str):
    return word.lower() in ('please', 'please,', ',', 'damn', 'shit')
