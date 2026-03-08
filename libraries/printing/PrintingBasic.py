import re
from libraries.printing.PrintingColor import Color

class PrintingBasic:

    def __init__(self) -> None:
        pass

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
        return [Color.RED, Color.GREEN, Color.YELLOW, Color.CYAN, Color.MAGENTA]

    @staticmethod
    def completeString(string: str, length: int, completeWith: str=' ') -> str:
        if len(string) < length:
            string += completeWith*(length-len(string))
        return string
    