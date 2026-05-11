from datetime import datetime
import re
from itertools import islice
from libraries.printing.PrintingColor import Color
from collections.abc import Iterable, Mapping

class PrintingBasic:

    def __init__(self) -> None:
        pass

    @staticmethod
    def checkAndPrepareValues(values: list|dict) -> list|dict:
        """
        Replace `None` values with `0`.

        Notes:
        - `dict.values()` returns `dict_values` (not `list`), so we treat any non-string iterable as a sequence.
        - When a dict is provided, a new sanitized dict is returned.
        """
        def _normalize(value):
            if value is None:
                value = 0
            if isinstance(value, (int, float)):
                return float(value)
            if isinstance(value, str):
                return float(PrintingBasic.intOrFloatString(value))
            try:
                return float(value)
            except (TypeError, ValueError):
                return value

        if values is None:
            return []

        if isinstance(values, Mapping):
            return {k: _normalize(v) for k, v in values.items()}

        if isinstance(values, (list, tuple)):
            return [_normalize(v) for v in values]

        if isinstance(values, Iterable) and not isinstance(values, (str, bytes)):
            return [_normalize(v) for v in list(values)]

        return values

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
    
    @staticmethod
    def getLastNElements(dictionary: dict, n: int=10):
        last_n_reversed = list(islice(reversed(dictionary.items()), 0, n))
        last_n_ordered = list(reversed(last_n_reversed))
        return dict(last_n_ordered)
    
    @staticmethod
    def getMonthFromValue(dateString: str):
        if (PrintingBasic.is_valid_date(dateString, '%d-%m-%Y')):
            return (dateString.split('-'))[1]
        if (PrintingBasic.is_valid_date(dateString, '%d/%m/%Y')):
            return (dateString.split('/'))[1]
        if (PrintingBasic.is_valid_date(dateString, '%m-%d-%Y')):
            return (dateString.split('-'))[0]
        if (PrintingBasic.is_valid_date(dateString, '%m/%d/%Y')):
            return (dateString.split('/'))[0]
        if (PrintingBasic.is_valid_date(dateString, '%Y-%m-%d')):
            return (dateString.split('-'))[1]
        if (PrintingBasic.is_valid_date(dateString, '%Y-%d-%m')):
            return (dateString.split('-'))[2]
        if (PrintingBasic.is_valid_date(dateString, '%Y/%m/%d')):
            return (dateString.split('/'))[1]
        if (PrintingBasic.is_valid_date(dateString, '%Y/%d/%m')):
            return (dateString.split('/'))[2]
        return False

    @staticmethod
    def is_valid_date(date_str, format_str):
        try:
            datetime.strptime(date_str, format_str)
            return True
        except ValueError:
            return False
