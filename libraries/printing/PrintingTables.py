from libraries.printing.PrintingBasic import PrintingBasic

class PrintingTable:

    def __init__(self) -> None:
        pass

    @staticmethod
    def printDictionaryAsTable(dataSet: list, columnsToShow: list = []):

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

                        length = len(column) if len(column) > len(columnName) else len(columnName)
                        if columnName in maximums.keys(): 
                            if length > maximums[columnName]:
                                maximums[columnName] = length
                        else:
                            maximums[columnName] = length

                        tableWidth += (2 + length)

                        headCell = (" "+columnName+" ") if len(columnName) > maximums[columnName] else (' '+columnName+' '*(maximums[columnName] - len(columnName)))
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
            print(" There is no data to print ")
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
    