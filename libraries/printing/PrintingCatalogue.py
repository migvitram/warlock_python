from libraries.printing.PrintingBasic import PrintingBasic

class PrintingCatalogue(PrintingBasic):

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def printCatalogueFromDictionary(dictionary: dict, depthLimit: int = 5):
        string = PrintingCatalogue.returnDictionaryIndecesAsString(dictionary, '|', depthLimit)
        print("Catalogue contents : ")
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
