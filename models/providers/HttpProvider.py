import re
import urllib.request
import urllib.error
from urllib.parse import urlparse
import gzip
import zstandard as zstd
from models.helpers.JsonFiles import JsonFiles

class HttpProvider:

    headers = {}

    def __init__(self) -> None:
        self.headers = {
            'accept-encoding':        'gzip, deflate, br, zstd',
            'accept-language':        'uk-UA,uk;q=0.9',
            'sec-ch-ua':        '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
            'sec-fetch-mode':        'navigate',
            'sec-fetch-site':        'same-origin',
            'sec-fetch-user':        '?1',
            'upgrade-insecure-requests':'1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
        }

        pass

    def getHtmlByUrl(self, url: str) -> str:
        if HttpProvider.isHyperlink(url):
            try:
                request = urllib.request.Request(url, headers=self.headers)
                response = urllib.request.urlopen(request)
                return self.readDependsOnResponse(response)
            except urllib.error.HTTPError as e:
                print(f"HTTP Error: {e.code} - {e.reason}")
            except urllib.error.URLError as e:
                print(f"URL Error: {e.reason}")
                return ''
        else:
            print(f"Url \'{url}\'is not valid URL \n")
            return ''    
    
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

    @staticmethod
    def getDomainFromUrl(url: str) -> str:
        parsed_url = urlparse(url)
        return parsed_url.netloc
    
    def readDependsOnResponse(self, response):
        if response.info().get('Content-Encoding') == 'gzip':
            with gzip.GzipFile(fileobj=response) as gzip_file:
                content_bytes = gzip_file.read()
                return content_bytes.decode('utf-8')
        elif response.info().get('Content-Encoding') == 'zstd':
            uncompressed_data = zstd.ZstdDecompressor().decompress(response.read(), max_output_size=100*1024*1024)
            return uncompressed_data
        else:
            content_bytes = response.read()
            return content_bytes.decode('utf-8')