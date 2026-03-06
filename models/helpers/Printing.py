import re
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

            deviderLine = ''
            maximums = {}
            tableWidth = 0
            tableHeadCells = {}
            tableHead = ''

            # get alignement
            for row in dataSet:
                for columnName, column in row.items():
                    if columnName in columnsToShow or len(columnsToShow) == 0:

                        column = Printing.prepareColumnTextForTable(column)    

                        length = len(column) if len(column) > len(columnName) else len(columnName)
                        if columnName in maximums.keys(): 
                            if length > maximums[columnName]:
                                maximums[columnName] = length
                        else:
                            maximums[columnName] = length

                        tableWidth += (2 + length)

                        headCell = (" "+columnName+" ") if len(columnName) > maximums[columnName] else (' '+columnName+' '*(maximums[columnName] - len(columnName)))
                        tableHeadCells[columnName] = headCell

            deviderLine = Printing.makeTableDeviderLine(tableHeadCells)
            straightLine = '-'*len(deviderLine)
            tableHead = Printing.makeTableHead(tableHeadCells)

            print(straightLine)
            print(tableHead)
            print(deviderLine)

            # and print
            for row in dataSet:

                rowToPrint = '| '
                
                for columnName, column in row.items():
                    if columnName in columnsToShow or len(columnsToShow) == 0:
                        column = Printing.prepareColumnTextForTable(column)    
                        
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
            columnsLimit: int = 20, shrinkTheColumnName: bool = True, step: int|float = 1,
            beginFromZero: bool = False
        ):
        hl = horizontalLine
        chartParams = {'max_X': 0.0, 'min_X': 0.0}
        chart = {"first":''}
        columnLength = 3
        columnsSeparator = ' | '
        shrinkTheKey = 0
        screenWidth = 250

        chartParams['max_X'] = Printing.intOrFloatString(str(max(dictionary.values())))
        chartParams['min_X'] = 0 if beginFromZero else Printing.intOrFloatString(str(min(dictionary.values())))

        step = Printing.chooseStep(chartParams['max_X'], chartParams['min_X'])
            
        for key, item in dictionary.items():
            # get min and max of X, get number of Y points
            # draw by lines: line got X value, space, X axe line, space, spaces*to_the_point, point,
            #   and the other spaces*till_the_end_of_line

            columnLength = len(str(key)) if len(str(key)) > 3 else columnLength  # '__|_dot_|_'
            # chart[0] = 
            # spaces_from_axe_to_end = axe_Y_number*Y_column_length + 2 space + 1 "|"

            if len(str(key)) * len(dictionary.items()) > screenWidth: # if len(columnText)*columnsNumber > 10*12
                shrinkTheKey = -(columnLength//2)
        
        # delta = float(chartParams['max_X']) - float(chartParams['min_X'])
        #step = 1.0   # depends on scale value

        current = Printing.getRoundedValue(chartParams['max_X'], step)
        lastOne = Printing.getRoundedValue(chartParams['min_X'], step) - 2*step
        maxValueLength = len(str(chartParams['max_X']))
        keyLength = Printing.getLengthLongestListItem(dictionary.keys(), shrinkTheKey)

        areaWidth = (keyLength+len(columnsSeparator))*len(dictionary.keys())
        firstLine = hl*maxValueLength + " | " + hl*(areaWidth)
        chart[str(current+step)] = firstLine

        while current > lastOne:
            beautifulKey = Printing.completeString(str(current), maxValueLength)
            if showOnlyDotValues:
                newLine = (beautifulKey if current in dictionary.values() else hl*maxValueLength) + " | "
            else:
                newLine = beautifulKey + " | "
            
            for k,v in dictionary.items():
                v = float(v)
                if(Printing.getRoundedValue(v, step) == current): # v need to round to the step value
                    newLine += Printing.alignDotInCenter(keyLength, hl, Printing.GREEN) + hl*len(columnsSeparator)
                else:
                    newLine += hl*keyLength + hl*len(columnsSeparator)
                    
            chart[str(current)] = chart[str(current)] + newLine if str(current) in chart else newLine
            current = round(current - step, 5)

        chart['basic'] = ' '*maxValueLength + " | " + Printing.convertListToString(dictionary.keys(), columnsSeparator, shrinkTheKey)

        print("\n")
        print("-" * (len(chartName)+keyLength if len(chartName) > areaWidth else keyLength + 3 + areaWidth))
        print(" " * 10 + chartName)
        print("-" * (len(chartName)+keyLength if len(chartName) > areaWidth else keyLength + 3 + areaWidth))

        for line in chart:
            print(chart[line])
        print("\n")

    @staticmethod
    def printDictionaryAsMultiChart(
        chartName: str, listOfDictionaries: list[dict]|dict[str, dict], 
        axesNames: dict = {}, horizontalLine: str = '_', showOnlyDotValues: bool = True,
        columnsLimit: int = 20, shrinkTheColumnName: bool = True, step: int|float = 1,
        beginFromZero: bool = False
        ):
        hl = horizontalLine
        lineNames = []
        if isinstance(listOfDictionaries, dict):
            lineNames = list(listOfDictionaries.keys())
            listOfDictionaries = list(listOfDictionaries.values())
        chartParams = {'max_X': 0.0, 'min_X': min( listOfDictionaries[0].values())}
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
            valuesX = dictionary.values()
            # dictionary with separeted color
            
            chartParams['max_X'] = max(valuesX) if max(valuesX) > chartParams['max_X'] else chartParams['max_X']
            chartParams['min_X'] = min(valuesX) if min(valuesX) < chartParams['min_X'] else chartParams['min_X']

            areaWidth = (keyLength+len(columnsSeparator))*len(dictionary.keys())
            keyLength = Printing.getLengthLongestListItem(dictionary.keys())

            for key, item in dictionary.items():
                # get min and max of X, get number of Y points
                # draw by lines: line got X value, space, X axe line, space, spaces*to_the_point, point,
                #   and the other spaces*till_the_end_of_line

                columnLength = len(str(key)) if len(str(key)) > 3 else columnLength  # '__|_dot_|_'
                # chart[0] = 
                # spaces_from_axe_to_end = axe_Y_number*Y_column_length + 2 space + 1 "|"

        step = Printing.chooseStep(float(chartParams['max_X']), float(chartParams['min_X']))
        current = Printing.getRoundedValue(float(chartParams['max_X']), step)
        lastOne = Printing.getRoundedValue(float(chartParams['min_X']), step) - 2*step
        maxValueLength = len(str(Printing.getRoundedValue(float(chartParams['max_X']), step)))

        firstLine = hl*maxValueLength + "_|" + hl*(areaWidth)
        chart[str(current+step)] = firstLine

        while current > lastOne:

            beautifulKey = Printing.completeString(str(current), maxValueLength)
            if showOnlyDotValues:
                newLine = beautifulKey + " |"
            else:
                newLine = hl*maxValueLength + " |"

            for date in valuesY:
            
                resultCell = ''
                dotsInCell = 0
                for dictIndex, dictionary in enumerate(listOfDictionaries):

                    if Printing.getRoundedValue(dictionary[date], step) == current:
                        dotsInCell += 1
                        resultCell += Printing.colorDot(Printing.getColorsList()[dictIndex])

                newLine += hl + Printing.alignedDots(keyLength, dotsInCell, resultCell)
                    
            chart[str(current)] = chart[str(current)] + newLine if str(current) in chart else newLine
            current = round(current - step, 5)

        chart['basic'] = ' '*maxValueLength + " | " + Printing.convertListToString(valuesY, columnsSeparator)

        print("\n")
        print("-" * (len(chartName)+keyLength if len(chartName) > areaWidth else keyLength + 3 + areaWidth))
        print(" " * 10 + chartName)
        print("-" * (len(chartName)+keyLength if len(chartName) > areaWidth else keyLength + 3 + areaWidth))

        for line in chart:
            print(chart[line])
        print("\n")
        
        # print the legend
        if len(lineNames) > 0:
            Printing.printTheLegendFromList(lineNames)
        pass

    @staticmethod
    def convertDictToString(dictionary: dict|list) -> str:
        if isinstance(dictionary, dict):
            return " { dictionary } "
        if isinstance(dictionary, list):
            return " [ list ] "
        return "..."

    @staticmethod
    def prepareColumnTextForTable(column, displayLength: int=65) -> str:
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
        return line*half + str(Printing.colorDot(color, 2)) + line*(stringLength - half - 1)

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
    def convertListToString(list, separator: str='|', shrinkTheKey = 0) -> str:
        if shrinkTheKey == 0:
            return separator.join(str(val) for val in list)
        else:
            return separator.join(str(val[:shrinkTheKey]) for val in list)

    @staticmethod
    def getLengthLongestListItem(list, shrinkTheKey = 0) -> int:
        longest = 0
        for k in list:
            longest = len(str(k))+shrinkTheKey if len(str(k))+shrinkTheKey > longest else longest
        return longest

    # black Dot for charts with Unicode 
    @staticmethod
    def blackDot(size: int=2) -> str:
        return Printing.colorDot(False, size)

    @staticmethod
    def colorDot(color: str|bool = False, size: int=2):
        preparedColor = ''
        reset = ''
        if color in Printing.getColorsList():
            preparedColor = color
            reset = Printing.RESET
            
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
    def printTheLegendFromList(lineNames: list):
        print("Chart legend:")
        for index, lineName in enumerate(lineNames):
            print("  " + Printing.colorDot(Printing.getColorsList()[index])+" - "+lineName)
        pass

    @staticmethod
    def getRoundedValue(valueToRound: int|float, step: int|float, roundPlace: str='tens', roundUp: bool=True):
        if step >= 1:
            leftOvers = valueToRound%step
            if leftOvers > (step*0.4):
                return valueToRound - leftOvers + step
            else:
                return valueToRound - leftOvers
        else:
            leftOvers = round(valueToRound%step, 4)
            if leftOvers > round((step*0.4), 4):
                return round(valueToRound - leftOvers + step, 4)
            else:
                return round(valueToRound - leftOvers, 4)

    @staticmethod
    def completeString(string: str, length: int, completeWith: str=' ') -> str:
        if len(string) < length:
            string += completeWith*(length-len(string))
        return string

    @staticmethod
    def intOrFloatString(stringToCheck: str) -> int|float:
        if stringToCheck is float or stringToCheck is int:
            return stringToCheck
        variant1 = re.findall(r"(\d+\.\d+)", stringToCheck)
        variant2 = re.findall(r"(\d+\,\d+)", stringToCheck)
        variant3 = re.findall(r"(\d+)", stringToCheck)
        if variant1:
            return float(variant1.pop())
        if variant2:
            return float(str(variant2.pop()).replace(',', '.'))
        if variant3:
            return int(variant3.pop())
        if len(stringToCheck) == 0:
            return 0
        else:
            return 0

    @staticmethod
    def getColorsList():
        return [Printing.RED, Printing.GREEN, Printing.YELLOW, Printing.CYAN]

    @staticmethod
    def chooseStep(maxValue, minValue) -> int|float:
        step = 1
        difference = maxValue - minValue
        if difference == 0 or difference < 0:
            return 1
        if difference > 1000:
            step = 100
        if difference <= 1000 and difference > 100:
            step = 50
        if difference <= 100 and difference > 50:
            step = 10
        if difference <= 50 and difference > 10: # default value
            step = 1
        if difference <= 10 and difference > 2:
            step = 0.5
        if difference <= 2 and difference > 1:
            step = 0.1
        if difference < 1 and difference > 0:
            step = 0.01
        return step
