import requests
from urllib import request

from requests import Response
from pyquery import PyQuery
from typing import Dict, Tuple
from library import FourSharedLibs
from dekimashita import Dekimashita
from icecream import ic
from utils import *

class FourShared(FourSharedLibs):
    def __init__(self, save: bool) -> None:
        super().__init__(save)
        ...

    def extract(self, url: str, item: int = 0) -> None:
        response: Response = self.api.get(url=url)
        html = PyQuery(response.text)

        title = html.find('h1.fileName').text()

        path = f'{self.create_dir(format="json")}/{title.split(".")[0].replace(" ", "_")}.json'

        (size, posted, types) = self.extract_navbar(html)
        (name_documents, url_documents) = self.collect_document(html.find('#moreFilesIFrame').attr('src'))

        headers = {
            "link": self.link,
            "domain": self.domain,
            "tag": [PyQuery(tag).text() for tag in html.find('#tagsDiv a')] + [self.domain],
            "crawling_time": now(),
            "crawling_time_epoch": epoch(),
            "path_data_raw": path,
            "path_data_document": "path_document",
            "path_data_clean": convert_path(path),
            "detail": {
                "title": title,
                "owner": html.find('a.fileOwner').text(),
                "size": size,
                "posted": posted,
                "type": types,
                "description": html.find('#fileDescriptionText').text()
            },
            "documents": name_documents
        }

        headers = self.download(html=html, header=headers)

        # self.update_cookies()


        File.write_json(path, headers)

        if not item:
            for index, url in enumerate(url_documents):
                ic(url)
                self.extract(url=url, item=index+1)
                ...

        ...
    
    def main(self) -> None:
        self.extract(self.link)


        ...



