class Drawing:

    def __init__(self) -> None:
        pass

    @staticmethod
    def displayTheImage(fileName: str):
        try:
            someImage = open(fileName)
            print(someImage.read())
        except:
            print("________----image " + fileName + "----________")
