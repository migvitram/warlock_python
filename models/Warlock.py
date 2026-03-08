import time
from models.PersonalSettings import Settings
from models.helpers.Drawing import Drawing
from models.helpers.Logger import Logger
from abilities import checkTheWish
from abilities import checkWishmasterSatisfied

class Warlock:

    def __init__(self) -> None:
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
        whatToDo = input("What do you want me to do? \n\n")
        checkTheWish(whatToDo)
        return

    def checkWishmasterSatisfied(self):
        
        wishes = True

        while wishes == True:
            want = input("Do you want something more? \n")
            if checkWishmasterSatisfied(want):
                print("Gooood...")
                time.sleep(1)
                print("Call me, any time to make your wish come true...")
                wishes = False
                exit
            else:
                checkTheWish(want)
        return