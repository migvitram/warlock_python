import os
from models.helpers.JsonFiles import JsonFiles
from models.helpers.Printing import Printing
from libraries.printing.PrintingColor import Color
from models.providers.scraping.YouTubeProvider import YouTubePvovider

class YouTubeNewsController:

    jsonFileStorage = ''
    pages = []
    provider: YouTubePvovider

    def __init__(self) -> None:
        storageFile = 'storage/youtube_pages.json'
        self.jsonFileStorage = os.path.abspath(storageFile)
        JsonFiles.runSelfDiagnostics(self.jsonFileStorage)
        pages = []
        self.provider = YouTubePvovider()

    def addChannelForTracking(self, pageName: str, url: str):
        storedData = JsonFiles.readDataFromJsonFile(self.jsonFileStorage)

        if pageName not in storedData:
            storedData[pageName] = {'url': url, 'newestVideo': {'videoName': '', 'date': ''}}
            JsonFiles.writeToTheLocalJsonStorage(storedData, self.jsonFileStorage)
        else:
            Printing.print("There is already exists channel with name !")
        
    def removeChannelByName(self, pageToDeleteName: str):
        storedData = JsonFiles.readDataFromJsonFile(self.jsonFileStorage)
        result = False
        # TODO : need to add the improvement for the dict using case !!!!!!
        for pageName, page in storedData.items():
            if pageName == pageToDeleteName:
                del storedData[pageName]
                JsonFiles.writeToTheLocalJsonStorage(storedData, self.jsonFileStorage)
                result = True
                break
            else:
                result = False
        if result == False:
            Printing.print("Can not find page \'"+pageToDeleteName+"\' ", Color.RED)

    def printSummary(self):
        summary = []
        for name, item in JsonFiles.readDataFromJsonFile(self.jsonFileStorage).items():
            summary.append({
                'pageName': name, 
                'newestVideo': item['newestVideo']['videoName'], 
                'date': item['newestVideo']['date']
            })
        Printing.printDictionaryAsTable(summary)

    def runTheCheckout(self):

        pages = JsonFiles.readDataFromJsonFile(self.jsonFileStorage)

        for pageName, data in pages.items():
            # get url, run the providers scraping method
            url = data['url']

            self.provider.setPage(url)
            video = self.provider.getLastVideos()
            data['newestVideo']['videoName'] = video['videoName']
            data['newestVideo']['date'] = video['date']

        JsonFiles.writeToTheLocalJsonStorage(pages, self.jsonFileStorage)
        