import bs4
from bs4 import BeautifulSoup as BS
import re
from models.helpers.Logger import Logger

class SoupHelper:

    @staticmethod
    def checkElementTextEquals(element: bs4.element.Tag|None, textToCompare: str):
        if isinstance(element, bs4.element.Tag):
            string = re.sub(r'[^\w]', '', str(element.get_text()))
            compare = re.sub(r'[^\w]', '', textToCompare)
            return string.strip().lower() == compare.strip().lower()
        else:
            return False
        
    @staticmethod
    def trimText(text: str) -> str:
        return text.strip()
    
    @staticmethod
    def trimNumberText(numberText: str) -> int|float:

        replacements = {
            '&nbsp;': '',
            ' ': '',
            '   ': '',
        }

        for search, replace in replacements.items():
            numberText = numberText.replace(search, replace)

        return int(numberText.strip())
