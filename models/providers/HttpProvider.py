import re
import urllib.request

class HttpProvider:

    def __init__(self) -> None:
        pass

    @staticmethod
    def getHtmlByUrl(url: str) -> str:
        if HttpProvider.isHyperlink(url):
            rawHtml = urllib.request.urlopen(url)
            return rawHtml.read().decode('utf-8')
        else:
            print("Url \'"+url+"\'is not valid URL \n")
            return ''    
            pass
    
    @staticmethod
    def isHyperlink(url: str) -> bool:
        # A simple regex for http/https URLs
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|\\'
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        return bool(regex.match(url))
