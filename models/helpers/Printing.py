class Printing:

    def __init__(self) -> None:
        pass
        
    @staticmethod
    def printDictionaryAsTable(dataSet: list, columnsToShow: list = []):

        if len(dataSet) > 0:

            devider = ''
            maximums = {}
            tableWidth = 0
            tableHeadCells = {}
            tableHead = ''

            # get alignement
            for row in dataSet:
                for columnName, column in row.items():
                    if columnName in columnsToShow:

                        if isinstance(column, dict) or isinstance(column, list):
                            column = Printing.convertDictToString(column)

                        length = len(column) if len(column) > len(columnName) else len(columnName)
                        if columnName in maximums.keys(): 
                            if length > maximums[columnName]:
                                maximums[columnName] = length
                        else:
                            maximums[columnName] = length

                        tableWidth += (2 + length)

                        headCell = (" "+columnName+" ") if len(columnName) > maximums[columnName] else (' '+columnName+' '*(maximums[columnName] - len(columnName)))
                        tableHeadCells[columnName] = headCell

            devider = Printing.makeTableDeviderLine(tableHeadCells)
            straightLine = '-'*len(devider)
            tableHead = Printing.makeTableHead(tableHeadCells)

            print(straightLine)
            print(tableHead)
            print(devider)

            # and print
            for row in dataSet:

                rowToPrint = '| '
                
                for columnName, column in row.items():
                    if columnName in columnsToShow:
                            
                        if isinstance(column, dict) or isinstance(column, list):
                            column = Printing.convertDictToString(column)

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
    def printDictionaryAsChart(
            chartName: str, dictionary: dict, 
            axesNames: dict = {}, horizontalLine: str = '_', showOnlyDotValues: bool = True,
            columnsLimit: int = 20, shrinkTheColumnName: bool = True, step: float = 1.0,
            beginFromZero: bool = False
        ):
        hl = horizontalLine
        chartParams = {'max_X': 0.0, 'min_X': 0.0}
        chart = {"first":''}
        columnLength = 3
        columnsSeparator = ' | '

        chartParams['max_X'] = max(dictionary.values())
        chartParams['min_X'] = 0.0 if beginFromZero else min(dictionary.values())
            
        for key, item in dictionary.items():
            # get min and max of X, get number of Y points
            # draw by lines: line got X value, space, X axe line, space, spaces*to_the_point, point,
            #   and the other spaces*till_the_end_of_line

            columnLength = len(str(key)) if len(str(key)) > 3 else columnLength  # '__|_dot_|_'
            # chart[0] = 
            # spaces_from_axe_to_end = axe_Y_number*Y_column_length + 2 space + 1 "|"
        
        # delta = float(chartParams['max_X']) - float(chartParams['min_X'])
        #step = 1.0   # depends on scale value

        current = float(chartParams['max_X'])
        lastOne = float(chartParams['min_X']) - 2
        maxValueLength = len(str(float(chartParams['max_X'])))
        keyLength = Printing.getLengthLongestListItem(dictionary.keys())

        areaWidth = (keyLength+len(columnsSeparator))*len(dictionary.keys())
        firstLine = hl*maxValueLength + " | " + hl*(areaWidth)
        chart[str(current+step)] = firstLine

        while current > lastOne:
            if showOnlyDotValues:
                newLine = (str(current) if current in dictionary.values() else hl*maxValueLength) + " | "
            else:
                newLine = str(current) + " | "
            
            for k,v in dictionary.items():
                v = float(v)
                if(v == current):
                    newLine += Printing.alignDotInCenter(keyLength, hl) + hl*len(columnsSeparator)
                else:
                    newLine += hl*keyLength + hl*len(columnsSeparator)
                    
            chart[str(current)] = chart[str(current)] + newLine if str(current) in chart else newLine
            current -= step

        chart['basic'] = ' '*maxValueLength + " | " + Printing.convertListToString(dictionary.keys(), columnsSeparator)

        print("\n")
        print("-" * (len(chartName)+keyLength if len(chartName) > areaWidth else keyLength + 3 + areaWidth))
        print(" " * 10 + chartName)
        print("-" * (len(chartName)+keyLength if len(chartName) > areaWidth else keyLength + 3 + areaWidth))

        for line in chart:
            print(chart[line])
        print("\n")

    @staticmethod
    def convertDictToString(dictionary: dict) -> str:
        result = ''
        for item, key in dictionary.items():
            result += str(key) + ' : ' + str(item) + ', '

        return result

    @staticmethod
    def alignDotInCenter(stringLength: int, line: str = '_'):
        half = stringLength//2
        return line*half + str(Printing.blackDot()) + line*(stringLength - half - 1)

    @staticmethod
    def convertListToString(list, separator: str='|') -> str:
        return separator.join(str(val) for val in list)

    @staticmethod
    def getLengthLongestListItem(list) -> int:
        longest = 0
        for k in list:
            longest = len(str(k)) if len(str(k)) > longest else longest
        return longest

    # black Dot for charts with Unicode 
    @staticmethod
    def blackDot(size: int=2) -> str:
        match size:
            case 1: return "\u2022"
            case 3: return "\u2B24"
            case _: return "\u25CF"

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
