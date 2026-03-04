import math
from models.helpers.Logger import Logger

class Printing:

    # Colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

    def __init__(self) -> None:
        pass
        
    @staticmethod
    def print(text: str, color: bool|str=False, fParam: bool=False):
        if color != False and color in [Printing.RED, Printing.GREEN, Printing.YELLOW, Printing.CYAN]:
            print(f"{color}"+text+f"{Printing.RESET}"+" \n")
        else:
            print(text)

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
                    if columnName in columnsToShow or len(columnsToShow) == 0:

                        column = Printing.prepareColumnForTable(column)    

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
                    if columnName in columnsToShow or len(columnsToShow) == 0:
                        column = Printing.prepareColumnForTable(column)    
                        
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
            columnsLimit: int = 20, shrinkTheColumnName: bool = True, step: int = 1,
            beginFromZero: bool = False
        ):
        hl = horizontalLine
        chartParams = {'max_X': 0.0, 'min_X': 0.0}
        chart = {"first":''}
        columnLength = 3
        columnsSeparator = ' | '

        chartParams['max_X'] = max(dictionary.values())
        chartParams['min_X'] = 0.0 if beginFromZero else min(dictionary.values())

        difference = float(chartParams['max_X']) - float(chartParams['min_X'])
        if difference > 50 and difference < 100:
            step = 10
        if difference >= 100 and difference < 1000:
            step = 50
            
        for key, item in dictionary.items():
            # get min and max of X, get number of Y points
            # draw by lines: line got X value, space, X axe line, space, spaces*to_the_point, point,
            #   and the other spaces*till_the_end_of_line

            columnLength = len(str(key)) if len(str(key)) > 3 else columnLength  # '__|_dot_|_'
            # chart[0] = 
            # spaces_from_axe_to_end = axe_Y_number*Y_column_length + 2 space + 1 "|"
        
        # delta = float(chartParams['max_X']) - float(chartParams['min_X'])
        #step = 1.0   # depends on scale value

        current = Printing.getRoundedValue(float(chartParams['max_X']), step)
        lastOne = Printing.getRoundedValue(float(chartParams['min_X']), step) - 2*step
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
                if(Printing.getRoundedValue(v, step) == current): # v need to round to the step value
                    newLine += Printing.alignDotInCenter(keyLength, hl, Printing.GREEN) + hl*len(columnsSeparator)
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
    def printDictionaryAsMultiChart(
        chartName: str, listOfDictionaries: dict|list, 
        axesNames: dict = {}, horizontalLine: str = '_', showOnlyDotValues: bool = True,
        columnsLimit: int = 20, shrinkTheColumnName: bool = True, step: float = 1.0,
        beginFromZero: bool = False
        ):
        hl = horizontalLine
        chartParams = {'max_X': 0.0, 'min_X': min(listOfDictionaries[0].values())}
        chart = {"first":''}
        columnLength = 3
        columnsSeparator = ' | '
        keyLength = 0
        areaWidth = 0
        colors = {}
        valuesY = []

        # is it dictionary or list ???? {'line name' => {'date': number, ... }, 'line 2' => {}, ... }
        for dictionary in listOfDictionaries:

            valuesY = dictionary.keys()
            # dictionary with separeted color
            
            chartParams['max_X'] = max(dictionary.values()) if max(dictionary.values()) > chartParams['max_X'] else chartParams['max_X']
            chartParams['min_X'] = min(dictionary.values()) if min(dictionary.values()) < chartParams['min_X'] else chartParams['min_X']
            # chartParams['min_X'] = min(dictionary.values()) if min(dictionary.values()) < chartParams['min_X'] else chartParams['min_X']

            areaWidth = (keyLength+len(columnsSeparator))*len(dictionary.keys())
            keyLength = Printing.getLengthLongestListItem(dictionary.keys())

            for key, item in dictionary.items():
                # get min and max of X, get number of Y points
                # draw by lines: line got X value, space, X axe line, space, spaces*to_the_point, point,
                #   and the other spaces*till_the_end_of_line

                columnLength = len(str(key)) if len(str(key)) > 3 else columnLength  # '__|_dot_|_'
                # chart[0] = 
                # spaces_from_axe_to_end = axe_Y_number*Y_column_length + 2 space + 1 "|"

        current = float(chartParams['max_X'])
        lastOne = float(chartParams['min_X']) - 2
        maxValueLength = len(str(float(chartParams['max_X'])))

        firstLine = hl*maxValueLength + "_|" + hl*(areaWidth)
        chart[str(current+step)] = firstLine

        while current > lastOne:

            if showOnlyDotValues:
                newLine = str(current) + " |"
            else:
                newLine = hl*maxValueLength + " |"

            for date in valuesY:
            
                resultCell = ''
                dotsInCell = 0
                for dictIndex, dictionary in enumerate(listOfDictionaries):

                    if dictionary[date] == current:
                        dotsInCell += 1
                        resultCell += Printing.colorDot(Printing.getColorsList()[dictIndex])

                newLine += hl + Printing.alignedDots(keyLength, dotsInCell, resultCell)
                    
            chart[str(current)] = chart[str(current)] + newLine if str(current) in chart else newLine
            current -= step

        chart['basic'] = ' '*maxValueLength + " | " + Printing.convertListToString(valuesY, columnsSeparator)

        print("\n")
        print("-" * (len(chartName)+keyLength if len(chartName) > areaWidth else keyLength + 3 + areaWidth))
        print(" " * 10 + chartName)
        print("-" * (len(chartName)+keyLength if len(chartName) > areaWidth else keyLength + 3 + areaWidth))

        for line in chart:
            print(chart[line])
        print("\n")

        pass

    @staticmethod
    def convertDictToString(dictionary: dict|list) -> str:
        result = ''
        for item, key in dictionary.items():
            result += str(key) + ' : ' + str(item) + ', '

        return result

    @staticmethod
    def prepareColumnForTable(column, displayLength: int=65) -> str:
        if isinstance(column, dict) or isinstance(column, list):
            column = Printing.convertDictToString(column)
        else:
            column = str(column)
        column = Printing.shrinkStringForTable(column, displayLength)
        return column

    @staticmethod
    def shrinkStringForTable(string: str, displayLength: int=65):
        return string if len(string) < displayLength else string[0:displayLength-3]+'...'

    @staticmethod
    def alignDotInCenter(stringLength: int, line: str = '_', color: str|bool=False):
        half = stringLength//2
        return line*half + str(Printing.blackDot(2, color)) + line*(stringLength - half - 1)

    @staticmethod
    def alignedDots(length: int, dotsNumber: int, resultCell: str, line: str='_'):
        spaces = length - dotsNumber
        half = spaces//2
        return line*half + resultCell + (length-dotsNumber-half+2)*line 

    @staticmethod
    def alignWordInCenter(stringLength: int, word: str, line: str = '_') -> str:
        dotNumbers = int(len(word)//2)
        leftOvers = int(stringLength - dotNumbers)
        if leftOvers < 0:
            # shrink the word for one letter ?
            Logger.log("There is a problem with the word width during chart printing : ("+Printing.__call__.__name__+" : "+Printing.alignWordInCenter.__name__+")")
            Printing.print("There is more dots then the column width ! ! ! ", Printing.YELLOW)
            Printing.print("this is the problem when the word is colored dots in ASCII encode", Printing.YELLOW)
            return '*'*stringLength
        elif leftOvers == 1:
            return line + word
        elif leftOvers == 2:
            return line + word + line
        else: #leftOvers > 2:
            half = leftOvers//2
            return half*line + word + (stringLength - half)*line

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
    def blackDot(size: int=2, color: str|bool=False) -> str:
        preparedColor = ''
        reset = ''
        if color != False and color in [Printing.RED, Printing.GREEN, Printing.YELLOW, Printing.CYAN]:
            preparedColor = color
            reset = Printing.RESET
            
        match size:
            case 1: return preparedColor + "\u2022" + reset
            case 3: return preparedColor + "\u2B24" + reset
            case _: return preparedColor + "\u25CF" + reset

    @staticmethod
    def colorDot(color: str, size: int=2):
        preparedColor = ''
        reset = Printing.RESET
        if color in Printing.getColorsList():
            preparedColor = color
            
        match size:
            case 1: return preparedColor + "\u2022" + reset
            case 3: return preparedColor + "\u2B24" + reset
            case _: return preparedColor + "\u25CF" + reset
        pass

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
    def getRoundedValue(valueToRound: int|float, step: int, roundPlace: str='tens', roundUp: bool=True):
        if step > 1:
            leftOvers = valueToRound%step
            if leftOvers > (4*step/10):
                return valueToRound - leftOvers + step
            else:
                return valueToRound - leftOvers
        return float(math.ceil(valueToRound))

    def getColorsList():
        return [Printing.RED, Printing.GREEN, Printing.YELLOW, Printing.CYAN]
