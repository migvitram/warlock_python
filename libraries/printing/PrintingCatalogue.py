from libraries.printing.PrintingBasic import PrintingBasic

class PrintingCatalogue(PrintingBasic):

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def printCatalogueFromDictionary(dictionary: dict):
        string = PrintingCatalogue.returnDictionaryIndecesAsString(dictionary)
        print(string)

    @staticmethod
    def returnDictionaryIndecesAsString(catalogue: dict|list, prefix: str='') -> str:
        result = ''
        pile = {}
        if isinstance(catalogue, dict):
            pile = catalogue.items()
            
        if isinstance(catalogue, list):
            pile = enumerate(catalogue)
        
        for index, value in pile:
            result += prefix+str(index)+" \n"
            if isinstance(value, dict) or isinstance(value, list):
                result += PrintingCatalogue.returnDictionaryIndecesAsString(value, prefix + " | ")
        return result
