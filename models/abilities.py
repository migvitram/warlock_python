import os
import subprocess
from controllers.CheckProductController import CheckProductController
from controllers.FinanceServicesController import FinanceServices
from controllers.FuelPriceController import FuelPriceController
from controllers.YouTubeNewsController import YouTubeNewsController
from models.helpers.Logger import Logger
from models.helpers.Printing import Printing
from libraries.printing.PrintingColor import Color
from datetime import datetime
from models.PersonalSettings import Settings
from dotenv import load_dotenv
from monadas.translation import _

class Abilities:

    lang: str

    def __init__(self) -> None:
        load_dotenv()
        self.lang = os.getenv("APP_LANGUAGE", 'ua')
        if Settings.paramExists('lang'):
            self.lang = str(Settings.getParam('lang'))

    def checkWishmasterSatisfied(self, want: str) -> bool:
        sentence = list(filter(self.correctWord, str.split(want.lower())))
        if ('no' in sentence) or 'no,' in sentence or ('exit' in sentence) or ('exit,' in sentence):
            return True
        return False

    def checkTheWish(self, theWishText: str):
        # split the wish to the words
        jsonProductStoragePass = 'storage/products_to_check.json'
        sentence = str.split(theWishText)
        checkProduct = CheckProductController(jsonProductStoragePass)
        checkYoutube = YouTubeNewsController()

        if sentence[0] == 'exit' and len(sentence) == 1:
            Printing.print("Glory to you, Wishmaster! \n", Color.GREEN)
            return exit

        if len(sentence) > 1:

            iterator = filter(self.correctWord, sentence)
            sentence = list(iterator)

            if sentence[0] == 'do' and sentence[1] == 'not' and sentence[2] == 'show' and sentence[3] == 'logo' and sentence[4] == 'on' and sentence[5] == 'start':
                # make the setting to not to show the logo on startup
                Settings.updateParam('showLogo', False)
                pass
            
            if sentence[0] == 'fuel' and sentence[1] == 'check':
                contr = FuelPriceController()
                contr.checkPrices()

            if sentence[0] == 'check' and sentence[1] == 'youtube':
                checkYoutube.runTheCheckout()
                checkYoutube.printSummary()

            if sentence[0] == 'clean' or sentence[0] == 'clear' or sentence[0] == 'purge':
                if sentence[1] == 'log':
                    deleted = Logger.clean()
                    if deleted:
                        Printing.print('Log file removed successfuly.', Color.GREEN)

            if sentence[0] == 'make':
                if sentence[1] == 'tests' or sentence[1] == 'self-tests':
                    # resultStatus = os.system('cd ./tests && pytest')
                    try:
                        result = subprocess.run(
                            ['pytest'],
                            cwd='./tests', 
                            # check=True,  # will raise an Exception
                            text=True, capture_output=True, encoding='utf-8', errors='ignore'
                        )
                        if result.returncode == 0:
                            Printing.print("Tests passed successfully! Can be merge!", Color.GREEN)
                        else:
                            Printing.print("Tests FAILED! CAN NOT merge, or rebase or some else...", Color.RED)
                            print(f"{result.returncode=}")
                    except Exception as e:
                        print(e)

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
                        productName = self.askUntilAnswer(_('app', 'For what product?', self.lang)+" \n")
                        checkProduct.printTheProductPriceChart(productName)

                    if sentence[2] == 'summary' and sentence[3] == 'product' and sentence[4] == 'table':
                        checkProduct.printTheSummaryProductTable()

                    if sentence[2] == 'product' and sentence[3] == 'summary' and sentence[4] == 'table':
                        checkProduct.printTheSummaryProductTable()

                    if sentence[2] == 'product' and sentence[3] == 'details':
                        productName = self.askUntilAnswer("For what product? \n")
                        checkProduct.printTheProductDetailView(productName)

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
                            currencyName = self.askUntilAnswer('Please, enter the currency short name (usd, eur, bps) : ')
                            financeService.printTheCurrencyRateHistory(currencyName)
                        pass

                    if sentence[2] == 'fuel' and sentence[3] == 'price' and sentence[4] == 'history':
                        contr = FuelPriceController()
                        if len(sentence) > 5:
                            if sentence[5] == 'for' and len(sentence[6]) > 0:
                                fuelBrand = sentence[6].strip()
                                contr.printBrandPriceHistory(fuelBrand)
                                return
                        contr.printPriceHistory()
                        return

                    if sentence[2] == 'youtube' and sentence[3] == 'summary':
                        checkYoutube.printSummary()
                        return

            if sentence[0] == 'add':
                if sentence[1] == 'the':
                    if sentence[2] == 'product' and sentence[3] == 'for' and sentence[4] == 'tracking':
                        productName = self.askUntilAnswer(_('app', "Please, enter the product name!", self.lang)+" \n")
                        productUrl = self.askUntilAnswer(_('app', "Please, enter the product URL!", self.lang)+" \n")
                        checkProduct.addProductForTracking(productName, productUrl)
                        pass

                    if sentence[2] == 'channel' and sentence[3] == 'for' and sentence[4] == 'tracking':
                        channelName = self.askUntilAnswer("Please, enter the channel name! \n")
                        channelUrl = self.askUntilAnswer("Please, enter the channel URL! \n")
                        checkYoutube.addChannelForTracking(channelName, channelUrl)
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
                        productName = self.askUntilAnswer(_('app', "Please, enter the name of the product you want to REMOVE!", self.lang)+" \n")
                        areYouSure = input("Are you sure, you want to delete product \""+productName+"\" from trackin? \n")
                        if areYouSure.lower() == 'yes' or areYouSure.lower() == 'y':
                            checkProduct.removeProductByName(productName)
                        else:
                            areYouSure = self.askUntilAnswer(_('app', "Please, enter \'yes\' or \'no\', or \'y\' or \'n\'", self.lang)+" \n")
                            if areYouSure.lower() == 'yes' or areYouSure.lower() == 'y':
                                checkProduct.removeProductByName(productName)

                    if sentence[2] == 'channel' and sentence[3] == 'for' and sentence[4] == 'tracking':
                        pageName = self.askUntilAnswer("Please, enter the name of the product you want to REMOVE! \n")
                        areYouSure = input("Are you sure, you want to delete product \""+pageName+"\" from trackin? \n")
                        if areYouSure.lower() == 'yes' or areYouSure.lower() == 'y':
                            checkYoutube.removeChannelByName(pageName)
                        else:
                            areYouSure = self.askUntilAnswer("Please, enter \"yes\" or \"no\", or \"y\" or \"n\" \n")
                            if areYouSure.lower() == 'yes' or areYouSure.lower() == 'y':
                                checkYoutube.removeChannelByName(pageName)
            for word in sentence:
                # print(word)
                pass

            # to see the construction to_verb -> the_noun
            # if sentence has one or more consturctions -> try to execute (set to the queue)

            # print('args type', type(sentence))
            # print(sentence)

            
        else:
            Printing.print("Please, clearify you wish, Wishmaster!", Color.YELLOW)
        return

    def askUntilAnswer(self, question: str) -> str:
        param = ''
        while param == '':
            param = input(question)
        return param

    # List of abbilities
    # to run the file, to write the text, to check the text by hyperlink and check some word/data
    # to search the specified data among text/news
    def knownComands(self) -> dict:
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

    def correctWord(self, word: str):
        return not self.wrongWord(word)

    def wrongWord(self, word: str):
        return word.lower() in ('please', 'please,', ',', 'damn', 'shit')
