from libraries.printing.PrintingBasic import PrintingBasic
from libraries.printing.PrintingColor import Color
from models.AppContext import AppContext
from monadas.translation import _

class PrintingText(PrintingBasic):

    def __init__(self) -> None:
        pass

    @staticmethod
    def print(text: str, color: bool|str=False, fParam: bool=False):
        if color != False and color in PrintingText.getColorsList():
            print(f"{color}"+_('app', text, str(AppContext.get('lang')))+f"{Color.RESET}"+" \n")
        else:
            print(text)

    