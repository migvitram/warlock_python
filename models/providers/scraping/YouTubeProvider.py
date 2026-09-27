import bs4
import re
from bs4 import BeautifulSoup as BS
from models.providers.HttpProvider import HttpProvider
from models.helpers.Printing import Printing
from libraries.printing.PrintingColor import Color
import json

class YouTubePvovider:

    requestResult = 'html'
    headers = {}
    soupObject: bs4.BeautifulSoup|bool
    page = ''

    def __init__(self, url:str|None = None) -> None:
        if url is not None:
            self.setPage(url)
        pass

    def setPage(self, page: str):
        if (HttpProvider.isHyperlink(page)):
            self.page = page
            self.fetchHtml(page)
            self.soupObject = BS(str(self.requestResult), 'html.parser')
        pass

    def getLastVideos(self):
        initContentName = "ytInitialData"
        contents = self.soupObject.find("script", text=re.compile(initContentName))

        if contents:
            # 2. Extract the text inside the script tag
            script_text = contents.string
            
            # 3. Use regex to capture the value inside the quotes
            match = re.search(r'var ytInitialData = (.*?);', script_text, re.DOTALL)

            if match:
                try:
                    a = json.loads(match.group(1))
                    videoTab = a['contents']['twoColumnBrowseResultsRenderer']['tabs'][1]
                    firstVideo = videoTab['tabRenderer']['content']['richGridRenderer']['contents'][0]['richItemRenderer']
                    videoMeta = firstVideo['content']['lockupViewModel']['metadata']['lockupMetadataViewModel']
                    videoName = videoMeta['title']['content']
                    videoDate = self.getVideoDate(videoMeta)
                    # print(f"{videoName=} {videoDate=}")
                    return {'videoName': videoName, 'date': videoDate}
                except Exception as e:
                    Printing.print(f"Error parsing Youtube JSON (maybe cause of structure) for {self.page}: {e}", Color.RED)
                    return {'videoName': self.page, 'date': 'error'}
            else:
                print(f"not match !")
                return {'videoName': self.page, 'date': 'error: not match'}
        pass

    def fetchHtml(self, url: str):
        if(HttpProvider.isHyperlink(url)):
            self.requestResult = HttpProvider().getHtmlByUrl(url)
            return self.requestResult
        else:
            return False

    def findElementByCssClass(self, tagName: str, cssClass: str) -> bs4.element.Tag|None:
        return self.soupObject.find(tagName, {'class': cssClass})
        
    def findElementByCssPath(self, cssPath: str) -> bs4.element.Tag|None:
        return self.soupObject.select_one(cssPath)

    def getVideoDate(self, videoMeta: dict) -> str:
        try:
            metaDataParts = videoMeta['metadata']['contentMetadataViewModel']['metadataRows'][0]['metadataParts']
            if len(metaDataParts) < 2: # means that video for sponsors
                return metaDataParts[0]['text']['content']
            else:
                return metaDataParts[1]['text']['content']
        except Exception as e:
            Printing.print(f"Error parsing Youtube video date, for {self.page}: {e}", Color.YELLOW)
            return ''
