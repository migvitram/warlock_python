import time
import traceback
from models.AppContext import AppContext
from models.PersonalSettings import Settings
from models.helpers.Drawing import Drawing
from models.helpers.Logger import Logger
from models.helpers.Printing import Printing
from libraries.printing.PrintingColor import Color
from models.abilities import Abilities
from monadas.translation import _

class Warlock:

    abilities: Abilities

    def __init__(self) -> None:
        # AppContext.set('lang', 'ua')
        AppContext.loadDefaultValues(Settings.readSettings())
        self.abilities = Abilities()
        self.printIntro()
        pass

    def printIntro(self):

        if Settings.getAsInt('visits') < 1 or not Settings.paramExists('showLogo'):
            Settings.updateParam('showLogo', True)

        # displayTheImage('storage/images/warlock_image_0003_120.txt')
        if Settings.getAsInt('visits') < 3:
            Drawing.displayTheImage('storage/images/warlock_image_0003_160.txt')
        else:
            print("\n")

        if self.checkToDisplayTheLogo():
            Drawing.displayTheImage('storage/images/warlock_word_0006_96_inv.txt')
        else:
            pass
        time.sleep(1)

        Printing.print("Warlock is listening...")
        time.sleep(1)

        Settings.revisit()
        pass

    def whatToDo(self):
        try:
            whatToDo = input(_('app', "What do you want me to do?", str(AppContext.get('lang'))) +"\n\n")
            self.abilities.checkTheWish(whatToDo)
            return
        except Exception as e:
            self.logAnError(e)

    def checkWishmasterSatisfied(self):
        
        wishes = True

        while wishes == True:
            try:
                want = input(_('app', "Do you want something more?", str(AppContext.get('lang'))) +"\n")
                if self.abilities.checkWishmasterSatisfied(want):
                    Printing.print("Gooood...")
                    time.sleep(1)
                    Printing.print("Call me, any time to make your wish come true...")
                    wishes = False
                    exit
                else:
                    self.abilities.checkTheWish(want)    
            except Exception as e:
                self.logAnError(e)
        return

    def checkToDisplayTheLogo(self) -> bool:

        if not Settings.paramExists('showLogo'):
            Settings.updateParam('showLogo', True)
            return True

        doDisplay = Settings.getStrict('showLogo')

        if doDisplay is True:
            return True
        elif( isinstance(doDisplay, int)):
            return int(doDisplay) > Settings.getAsInt('visits')
        else:
            return False
    
    def logAnError(self, e: Exception, message: str=''):
        Printing.print(f"There was an error during programm running : {e}. Check app.log file for more info.", Color.RED)
        Logger.log(f"Error : {e}" + "\n" + traceback.format_exc())
        return
