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
                        # print('running ... ')

        if sentence[0] == 'print':
            if sentence[1] == 'the':
                if sentence[2] == 'product' and sentence[3] == 'price' and sentence[4] == 'history':
                    checkProduct.printTheProductPriceChart(0)
                    # print('running ... ')

                if sentence[2] == 'summary' and sentence[3] == 'product' and sentence[4] == 'table':
                    checkProduct.printTheSummaryProductTable()

        if sentence[0] == 'add':
            if sentence[1] == 'the':
                if sentence[2] == 'product' and sentence[3] == 'for' and sentence[4] == 'tracking':
                    productName = input("Please, enter the product name! \n")
                    productUrl = input("Please, enter the product URL! \n")
                    checkProduct.addProductForTracking(productName, productUrl)
                    pass

        if sentence[0] == 'remove':
            if sentence[1] == 'the':
                if sentence[2] == 'product' and sentence[3] == 'for' and sentence[4] == 'tracking':
                    productName = input("Please, enter the name of the product you want to REMOVE! \n")
                    checkProduct.removeProductByName(productName)
                    pass

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
            print("Greating to you, Wishmaster! \n")
        else:
            print("Please, clearify you wish, Wishmaster! \n")
        exit

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

def isHyperlink(url_string):
    # A simple regex for http/https URLs
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|\\'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return bool(regex.match(url_string))

def correctWord(word: str):
    return not wrongWord(word)

def wrongWord(word: str):
    return word.lower() in ('please', 'please,', ',', 'damn', 'shit')
