from libraries.printing.PrintingBasic import PrintingBasic

class PrintingText:

    def __init__(self) -> None:
        pass

    @staticmethod
    def print(text: str, color: bool|str=False, fParam: bool=False):
        if color != False and color in PrintingBasic.getColorsList():
            print(f"{color}"+text+f"{PrintingBasic.RESET}"+" \n")
        else:
            print(text)

    