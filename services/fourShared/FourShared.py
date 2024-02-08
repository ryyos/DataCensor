import requests
from urllib import request

from requests import Response
from pyquery import PyQuery
from typing import Dict, Tuple
from library import FourSharedLibs
from icecream import ic

from utils import *

class FourShared(FourSharedLibs):
    def __init__(self, save: bool) -> None:
        super().__init__(save)
        ...


    def extract(self, url: str, item: int = 0) -> None:
        response: Response = self.api.get(url=url, headers=self.headers, cookies=self.cookies)
        html = PyQuery(response.text)

        (size, posted, types) = self.extract_navbar(html)

        path = self.create_dir(title=html.find('h1.fileName').text())

        headers = {
            "link": self.link,
            "domain": self.domain,
            "tag": [PyQuery(tag).text() for tag in html.find('#tagsDiv a')] + [self.domain],
            "crawling_time": now(),
            "crawling_time_epoch": epoch(),
            "path_data_raw": path,
            "path_data_clean": convert_path(path),
            "detail": {
                "title": html.find('h1.fileName').text(),
                "owner": html.find('a.fileOwner').text(),
                "size": size,
                "posted": posted,
                "type": types,
                "description": html.find('#fileDescriptionText').text()
            },
            "documents": self.collect_document(html.find('#moreFilesIFrame').attr('src'))
        }

        File.write_json
        
        ...
    
    def main(self) -> None:
        self.extract(self.link)


        ...
