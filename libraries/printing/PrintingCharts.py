from libraries.printing.PrintingBasic import PrintingBasic
from libraries.printing.PrintingColor import Color
from libraries.printing.PrintingText import PrintingText

class PrintingCharts(PrintingBasic):

    def __init__(self) -> None:
        pass

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

        chartParams['max_X'] = PrintingCharts.intOrFloatString(str(max(dictionary.values())))
        chartParams['min_X'] = 0 if beginFromZero else PrintingCharts.intOrFloatString(str(min(dictionary.values())))

        step = PrintingCharts.chooseStep(chartParams['max_X'], chartParams['min_X'])
            
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

        current = PrintingCharts.getRoundedValue(chartParams['max_X'], step)
        lastOne = PrintingCharts.getRoundedValue(chartParams['min_X'], step) - 2*step
        maxValueLength = len(str(chartParams['max_X']))
        keyLength = PrintingCharts.getLengthLongestListItem(dictionary.keys(), shrinkTheKey)

        areaWidth = (keyLength+len(columnsSeparator))*len(dictionary.keys())
        firstLine = hl*maxValueLength + " | " + hl*(areaWidth)
        chart[str(current+step)] = firstLine

        while current > lastOne:
            beautifulKey = PrintingCharts.completeString(str(current), maxValueLength)
            if showOnlyDotValues:
                newLine = (beautifulKey if current in dictionary.values() else hl*maxValueLength) + " | "
            else:
                newLine = beautifulKey + " | "
            
            for k,v in dictionary.items():
                v = float(v)
                if(PrintingCharts.getRoundedValue(v, step) == current): # v need to round to the step value
                    newLine += PrintingCharts.alignDotInCenter(keyLength, hl, Color.GREEN) + hl*len(columnsSeparator)
                else:
                    newLine += hl*keyLength + hl*len(columnsSeparator)
                    
            chart[str(current)] = chart[str(current)] + newLine if str(current) in chart else newLine
            current = round(current - step, 5)

        chart['basic'] = ' '*maxValueLength + " | " + PrintingCharts.convertListToString(dictionary.keys(), columnsSeparator, shrinkTheKey)

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
            keyLength = PrintingCharts.getLengthLongestListItem(dictionary.keys())

            for key, item in dictionary.items():
                # get min and max of X, get number of Y points
                # draw by lines: line got X value, space, X axe line, space, spaces*to_the_point, point,
                #   and the other spaces*till_the_end_of_line

                columnLength = len(str(key)) if len(str(key)) > 3 else columnLength  # '__|_dot_|_'
                # chart[0] = 
                # spaces_from_axe_to_end = axe_Y_number*Y_column_length + 2 space + 1 "|"

        step = PrintingCharts.chooseStep(float(chartParams['max_X']), float(chartParams['min_X']))
        current = PrintingCharts.getRoundedValue(float(chartParams['max_X']), step)
        lastOne = PrintingCharts.getRoundedValue(float(chartParams['min_X']), step) - 2*step
        maxValueLength = len(str(PrintingCharts.getRoundedValue(float(chartParams['max_X']), step)))

        firstLine = hl*maxValueLength + "_|" + hl*(areaWidth)
        chart[str(current+step)] = firstLine

        while current > lastOne:

            beautifulKey = PrintingCharts.completeString(str(current), maxValueLength)
            if showOnlyDotValues:
                newLine = beautifulKey + " |"
            else:
                newLine = hl*maxValueLength + " |"

            for date in valuesY:
            
                resultCell = ''
                dotsInCell = 0
                for dictIndex, dictionary in enumerate(listOfDictionaries):

                    if PrintingCharts.getRoundedValue(dictionary[date], step) == current:
                        dotsInCell += 1
                        resultCell += PrintingCharts.colorDot(PrintingCharts.getColorsList()[dictIndex])

                newLine += hl + PrintingCharts.alignedDots(keyLength, dotsInCell, resultCell)
                    
            chart[str(current)] = chart[str(current)] + newLine if str(current) in chart else newLine
            current = round(current - step, 5)

        chart['basic'] = ' '*maxValueLength + " | " + PrintingCharts.convertListToString(valuesY, columnsSeparator)

        print("\n")
        print("-" * (len(chartName)+keyLength if len(chartName) > areaWidth else keyLength + 3 + areaWidth))
        print(" " * 10 + chartName)
        print("-" * (len(chartName)+keyLength if len(chartName) > areaWidth else keyLength + 3 + areaWidth))

        for line in chart:
            print(chart[line])
        print("\n")
        
        # print the legend
        if len(lineNames) > 0:
            PrintingCharts.printTheLegendFromList(lineNames)
        pass

    @staticmethod
    def alignDotInCenter(stringLength: int, line: str = '_', color: str|bool=False):
        half = stringLength//2
        return line*half + str(PrintingCharts.colorDot(color, 2)) + line*(stringLength - half - 1)

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
            PrintingText.print("There is more dots then the column width ! ! ! ", Color.YELLOW)
            PrintingText.print("this is the problem when the word is colored dots in ASCII encode", Color.YELLOW)
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
        return PrintingCharts.colorDot(False, size)

    @staticmethod
    def colorDot(color: str|bool = False, size: int=2):
        preparedColor = ''
        reset = ''
        if color in PrintingCharts.getColorsList():
            preparedColor = color
            reset = Color.RESET
            
        match size:
            case 1: return preparedColor + "\u2022" + reset
            case 3: return preparedColor + "\u2B24" + reset
            case _: return preparedColor + "\u25CF" + reset
        pass

    @staticmethod
    def printTheLegendFromList(lineNames: list):
        print("Chart legend:")
        for index, lineName in enumerate(lineNames):
            print("  " + PrintingCharts.colorDot(PrintingCharts.getColorsList()[index])+" - "+lineName)
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
