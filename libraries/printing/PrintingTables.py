from libraries.printing.PrintingBasic import PrintingBasic
from models.AppContext import AppContext
from monadas.translation import _

class PrintingTable(PrintingBasic):

    def __init__(self) -> None:
        pass

    @staticmethod
    def printDictionaryAsTable(dataSet: list, columnsToShow: list = []):

        lang = str(AppContext.get('lang'))

        if len(dataSet) > 0:

            deviderLine = ''
            maximums = {}
            tableWidth = 0
            tableHeadCells = {}
            tableHead = ''

            # get alignement
            for row in dataSet:
                for columnName, column in row.items():
                    if columnName in columnsToShow or len(columnsToShow) == 0:

                        column = PrintingTable.prepareColumnTextForTable(column)    

                        preparedColumnName = _('app', columnName, str(AppContext.get('lang'))).strip()
                        # preparedColumnName = columnName
                        length = len(column) if len(column) > len(preparedColumnName) else len(preparedColumnName)
                        if columnName in maximums.keys(): 
                            if length > maximums[columnName]:
                                maximums[columnName] = length
                        else:
                            maximums[columnName] = length

                        tableWidth += (2 + length)

                        headCell = (" "+preparedColumnName) if len(preparedColumnName) > maximums[columnName] else (' '+preparedColumnName+' '*(maximums[columnName] - len(preparedColumnName)))
                        tableHeadCells[columnName] = headCell

            deviderLine = PrintingTable.makeTableDeviderLine(tableHeadCells)
            straightLine = '-'*len(deviderLine)
            tableHead = PrintingTable.makeTableHead(tableHeadCells)

            print(straightLine)
            print(tableHead)
            print(deviderLine)

            # and print
            for row in dataSet:

                rowToPrint = '| '
                
                for columnName, column in row.items():
                    if columnName in columnsToShow or len(columnsToShow) == 0:
                        column = PrintingTable.prepareColumnTextForTable(column)    
                        
                        rowToPrint += column
                        if len(column) < maximums[columnName]:
                            rowToPrint += ' ' * (maximums[columnName] - len(column))
                        rowToPrint += ' | '

                print(rowToPrint)
                
            print(straightLine)
        else:
            print("-" * 120)
            print("  "+_('app', "There is no data to print", lang)+"  ")
            print("-" * 120)

    @staticmethod
    def makeTableDeviderLine(tableHeadCellsDict: dict) -> str:
        devider = '|'
        for cell in tableHeadCellsDict.values():
            devider+='-'*(len(cell)+1)+'+'
        devider = devider[:-1] + '|'
        return devider

    @staticmethod
    def makeTableHead(tableHeadCellsDict: dict) -> str:
        return '|'+' |'.join(tableHeadCellsDict.values())+' |'

    @staticmethod
    def prepareColumnTextForTable(column, displayLength: int=65) -> str:
        if isinstance(column, dict) or isinstance(column, list):
            column = PrintingTable.convertDictToString(column)
        else:
            column = str(column)
        column = PrintingTable.shrinkStringForTable(column, displayLength)
        return column

    @staticmethod
    def shrinkStringForTable(string: str, displayLength: int=65):
        return string if len(string) < displayLength else string[0:displayLength-3]+'...'

    @staticmethod
    def convertDictToString(dictionary: dict|list) -> str:
        if isinstance(dictionary, dict):
            return " { dictionary } "
        if isinstance(dictionary, list):
            return " [ list ] "
        return "..."
    