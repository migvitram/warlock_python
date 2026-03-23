import time
import traceback
from models.AppContext import AppContext
from models.PersonalSettings import Settings
from models.helpers.Drawing import Drawing
from models.helpers.Logger import Logger
from models.helpers.Printing import Printing
from libraries.printing.PrintingColor import Color
from abilities import checkTheWish
from abilities import checkWishmasterSatisfied

class Warlock:

    def __init__(self) -> None:
        # AppContext.set('lang', 'ua')
        self.printIntro()
        pass

    def printIntro(self):
        # displayTheImage('storage/images/warlock_image_0003_120.txt')
        if Settings.getAsInt('visits') < 2:
            Drawing.displayTheImage('storage/images/warlock_image_0003_160.txt')
        else:
            print("\n")
        Drawing.displayTheImage('storage/images/warlock_word_0006_96_inv.txt')
        time.sleep(1)

        print("Warlock is listening... \n")
        time.sleep(1)

        Settings.revisit()
        pass

    def whatToDo(self):
        try:
            whatToDo = input("What do you want me to do? \n\n")
            checkTheWish(whatToDo)
            return
        except Exception as e:
            self.logAnError(e)

    def checkWishmasterSatisfied(self):
        
        wishes = True

        while wishes == True:
            try:
                want = input("Do you want something more? \n")
                if checkWishmasterSatisfied(want):
                    print("Gooood...")
                    time.sleep(1)
                    print("Call me, any time to make your wish come true...")
                    wishes = False
                    exit
                else:
                    checkTheWish(want)    
            except Exception as e:
                self.logAnError(e)
        return
    
    def logAnError(self, e: Exception, message: str=''):
        Printing.print(f"There was an error during programm running : {e}. Check app.log file for more info.", Color.RED)
        Logger.log(f"Error : {e}" + "\n" + traceback.format_exc())
        return