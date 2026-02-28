import bs4
from bs4 import BeautifulSoup as BS
import re

class SoupHelper:

    @staticmethod
    def checkTheProduct(rawHtml):
        soup = BS(rawHtml, 'html.parser')
        presenceCheckResult = SoupHelper.checkPresence(soup)
        absenceCheckResult = SoupHelper.checkAbsence(soup)

        if presenceCheckResult == False and absenceCheckResult == False:
            print("something went wrong, or there is no product status on the page")
            return False
        else:
            answer = 'Yes' if presenceCheckResult else 'No'
            return answer

    @staticmethod
    def checkPresence(soupObject, status='В наявності', tagName='span'):
        if isinstance(soupObject.find(tagName, text=status), bs4.element.Tag):
            return True
        else:
            return False

    @staticmethod
    def checkAbsence(soupObject, status='Немає в наявності', tagName='span'):
        if isinstance(soupObject.find(tagName, text=status), bs4.element.Tag):
            return True
        else:
            return False

    @staticmethod
    def checkThePrice(rawHtml):
        soup = BS(rawHtml, 'html.parser')

        soupObject = soup.find('div', {'class': 'price'})

        if isinstance(soupObject, bs4.element.Tag):
            text = soupObject.get_text()
            value = re.findall('\d+', text)
            return value[0] if len(value) > 0 else False
        else:
            return False

        