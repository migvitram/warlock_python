import bs4
from bs4 import BeautifulSoup as BS
from models.providers.HttpProvider import HttpProvider

class AbstractScrapingProvider:

    WALK_METHOD_BY_CSS_IDENTIFIER = 'css'
    WALK_METHOD_BY_NESTED_ELEMENTS = 'nested_element'
    
    GET_ELEMENT_BY_CSS_CLASS = 'css_class'
    GET_ELEMENT_BY_CSS_ID = 'css_id'
    GET_ELEMENT_BY_TEXT = 'css_text'

    requestResult = 'html'
    headers = {}
    soupObject: bs4.BeautifulSoup|bool
    
    productPrice = 0
    productPresence = False

    def __init__(self) -> None:
        self.soupObject = False
        pass

    def visitThePage(self, url: str):
        self.requestResult = self.fetchHtml(url)
        self.makeSoupObject()
        self.productPresence = self.fetchTheProductPresence()
        self.productPrice = self.fetchTheProductPrice()
        return True
    
    def makeSoupObject(self):
        if self.soupObject is False:
            self.soupObject = BS(str(self.requestResult), 'html.parser')
        return self.soupObject

    def fetchHtml(self, url: str):
        if(HttpProvider.isHyperlink(url)):
            self.requestResult = HttpProvider().getHtmlByUrl(url)
            return self.requestResult
        else:
            return False

    def checkElementPresentByText(self, elementText, tagName='span'):
        if isinstance(self.findElementByText(elementText, tagName), bs4.element.Tag):
            return True
        else:
            return False

    def findElementByText(self, elementText: str, tagName: str='span'):
        return self.soupObject.find(tagName, text=elementText)
    
    def findElementByCssClass(self, tagName: str, cssClass: str) -> bs4.element.Tag|None:
        return self.soupObject.find(tagName, {'class': cssClass})

    def fetchTheProductPrice(self):
        raise NotImplementedError('You need to implement the fetchTheProductPrice() of base abstract class')

    def fetchTheProductPresence(self):
        raise NotImplementedError('You need to implement the fetchTheProductPresence() of base abstract class')

    # def returnStructureWalkMethod(self):
        # raise NotImplementedError('You need to implement the returnStructureWalkMethod() of base abstract class')

    # def returnPricePath(self):
        # raise NotImplementedError('You need to implement the returnPricePath() of base abstract class')

    # def returnPresencePath(self):
        # raise NotImplementedError('You need to implement the returnPresencePath() of base abstract class')

    def returnTheProductPrice(self):
        return self.productPrice

    def returnTheProductPresence(self):
        return self.productPresence
    