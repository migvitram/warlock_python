from models.AppContext import AppContext
from monadas.translation import _
from libraries.printing.PrintingBasic import PrintingBasic

class PrintingCatalogue(PrintingBasic):

    lang = 'en'

    def __init__(self) -> None:
        super().__init__()
        self.lang = str(AppContext.get('lang'))

    @staticmethod
    def printCatalogueFromDictionary(dictionary: dict, depthLimit: int = 5):
        lang = str(AppContext.get('lang'))
        string = PrintingCatalogue.returnDictionaryIndecesAsString(dictionary, '|', depthLimit)
        print(_('app', "Catalogue contents", lang)+" : ")
        print(string)

    @staticmethod
    def returnDictionaryIndecesAsString(catalogue: dict|list, prefix: str='', depthLimit: int = 5) -> str:
        resultLine = ''
        pile = {}
        coursor = depthLimit-1

        if isinstance(catalogue, dict):
            pile = catalogue.items()
        if isinstance(catalogue, list):
            pile = enumerate(catalogue)
        
        for index, value in pile:
            resultLine += prefix+"-"+str(index)+" \n"
            if isinstance(value, dict) or isinstance(value, list):
                if coursor == 0:
                    resultLine += prefix+" | ... \n"
                else:
                    resultLine += PrintingCatalogue.returnDictionaryIndecesAsString(value, prefix + " |", coursor)
        return resultLine
