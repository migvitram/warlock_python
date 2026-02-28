import re
import os
from controllers.CheckProductController import CheckProductController

def checkWishmasterSatisfied(want: str) -> bool:
    sentence = list(filter(correctWord, str.split(want.lower())))
    if ('no' in sentence) or 'no,' in sentence or ('exit' in sentence) or ('exit,' in sentence):
        return True
    return False

def checkTheWish(theWishText: str):
    # split the wish to the words
    jsonProductStoragePass = 'storage/products_to_check.json'
    sentence = str.split(theWishText)

    if len(sentence) > 1:

        iterator = filter(correctWord, sentence)
        sentence = list(iterator)

        checkProduct = CheckProductController(jsonProductStoragePass)

        if sentence[0] == 'make':
            if sentence[1] == 'tests' or sentence[1] == 'self-tests':
                resultStatus = os.system('cd ./tests && pytest')

        if sentence[0] == 'run':
            if sentence[1] == 'the':
                if sentence[2] == 'product':
                    if sentence[3] == 'tracking':
                        checkProduct.run()

        if sentence[0] == 'print':
            if sentence[1] == 'demo':
                checkProduct.printDemo()
                pass
            if len(sentence) > 2 and sentence[1] == 'demo' and sentence[2] == 'table':
                checkProduct.printDemoTable()
                pass

            if sentence[1] == 'the':
                if sentence[2] == 'product' and sentence[3] == 'price' and sentence[4] == 'history':
                    productName = askUntilAnswer("For what product? \n")
                    checkProduct.printTheProductPriceChart(productName)

                if sentence[2] == 'summary' and sentence[3] == 'product' and sentence[4] == 'table':
                    checkProduct.printTheSummaryProductTable()

                if sentence[2] == 'product' and sentence[3] == 'summary' and sentence[4] == 'table':
                    checkProduct.printTheSummaryProductTable()

        if sentence[0] == 'add':
            if sentence[1] == 'the':
                if sentence[2] == 'product' and sentence[3] == 'for' and sentence[4] == 'tracking':
                    productName = askUntilAnswer("Please, enter the product name! \n")
                    productUrl = askUntilAnswer("Please, enter the product URL! \n")
                    checkProduct.addProductForTracking(productName, productUrl)
                    pass

        if sentence[0] == 'remove' or sentence[0] == 'delete':
            if sentence[1] == 'the':
                if sentence[2] == 'product' and sentence[3] == 'for' and sentence[4] == 'tracking':
                    productName = askUntilAnswer("Please, enter the name of the product you want to REMOVE! \n")
                    areYouSure = input("Are you sure, you want to delete product \""+productName+"\" from trackin? \n")
                    if areYouSure.lower() == 'yes' or areYouSure.lower() == 'y':
                        checkProduct.removeProductByName(productName)
                    else:
                        areYouSure = askUntilAnswer("Please, enter \"yes\" or \"no\", or \"y\" or \"n\" \n")
                        if areYouSure.lower() == 'yes' or areYouSure.lower() == 'y':
                            checkProduct.removeProductByName(productName)

        for word in sentence:
            # print(word)
            pass

        # to see the construction to_verb -> the_noun
        # if sentence has one or more consturctions -> try to execute (set to the queue)

        # print('args type', type(sentence))
        # print(sentence)

        pass
    else:
        if sentence[0] == 'exit':
            print("Greeting to you, Wishmaster! \n")
        else:
            print("Please, clearify you wish, Wishmaster! \n")
    exit

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
