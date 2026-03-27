from libraries.printing.PrintingCharts import PrintingCharts
from libraries.printing.PrintingText import PrintingText
from libraries.printing.PrintingTables import PrintingTable

class Printing:

    def __init__(self) -> None:
        pass
        
    @staticmethod
    def print(text: str, color: bool|str=False, fParam: bool=False):
        PrintingText.print(text, color, fParam)

    @staticmethod
    def printDictionaryAsTable(dataSet: list, columnsToShow: list = []):
        PrintingTable.printDictionaryAsTable(dataSet, columnsToShow)

    @staticmethod            
    def printDictionaryAsChart(
            chartName: str, dictionary: dict, 
            axesNames: dict = {}, horizontalLine: str = '_', showOnlyDotValues: bool = True,
            columnsLimit: int = 20, shrinkTheColumnName: bool = True, step = None
        ):
        PrintingCharts.printDictionaryAsChart(chartName, dictionary, axesNames, horizontalLine, showOnlyDotValues, columnsLimit, shrinkTheColumnName, step=step)

    @staticmethod
    def printDictionaryAsMultiChart(
        chartName: str, listOfDictionaries: list[dict]|dict[str, dict], 
        axesNames: dict = {}, horizontalLine: str = '_', showOnlyDotValues: bool = True,
        columnsLimit: int = 20, shrinkTheColumnName: bool = True, step = None
        ):
        PrintingCharts.printDictionaryAsMultiChart(chartName, listOfDictionaries, axesNames, horizontalLine, showOnlyDotValues, columnsLimit, shrinkTheColumnName, step=step)

