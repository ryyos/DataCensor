import requests
from urllib import request

from requests import Response
from pyquery import PyQuery
from typing import Dict, Tuple
from library import FourSharedLibs
from concurrent.futures import wait
from time import sleep
from typing import List
from icecream import ic

from dekimashita import Dekimashita
from utils import *

class FourShared(FourSharedLibs):
    def __init__(self, **kwargs) -> None:
        super().__init__(kwargs["save"])

        self.update_cookies()

        self.type_process = kwargs["type"]
        self.SAVE_TO_S3 = kwargs["s3"]
        self.SAVE_TO_LOKAL = kwargs["save"]
        self.USING_THREADS = kwargs["thread"]

        self.link = kwargs["url"]

        self.temp_path = None


    def extract(self, component: Tuple[str]) -> None:
        (url, item) = component

        response: Response = self.api.get(url=url)
        html = PyQuery(response.text)

        title: str = html.find('h1.fileName').text()
        if not title:
            title: str = html.find('div[class="generalFilename"]').text()

        folder: str = html.find('a[class="gaClick hideLong"]').text()
        if not folder:
            folder: str = self.temp_path

        self.temp_path = folder
        path: str = f'{self.create_dir(format="json", folder=folder.lower())}/{title.split(".")[0].replace(" ", "_")}.json'

        (size, posted, types) = self.extract_navbar(html)

        name_documents = None
        try:
            (name_documents, url_documents) = self.collect_document(html.find('#moreFilesIFrame').attr('src'))
        except Exception: ...

        headers = {
            "link": url,
            "domain": self.domain,
            "tag": [PyQuery(tag).text() for tag in html.find('#tagsDiv a')] + [self.domain],
            "crawling_time": now(),
            "crawling_time_epoch": epoch(),
            "path_data_raw": self.BASE_PATH+path,
            "path_data_document": "path_document",
            "path_data_clean": self.BASE_PATH+convert_path(path),
            "detail": {
                "title": title,
                "owner": html.find('a.fileOwner').text(),
                "size": size,
                "posted": posted,
                "type": types.replace(' ', ''),
                "description": html.find('#fileDescriptionText').text()
            },
        }

        if self.type_process == 'one':
            headers.update({
                "documents": name_documents
            })

        if self.SAVE_TO_LOKAL:
            headers = self.download(html=html, header=headers)
            File.write_json(path, Dekimashita.vdict(headers, '\n'))

        if not item and self.type_process == 'one':

            task_executors = []
            for index, url in enumerate(url_documents):
                
                component = (url, index+1)

                if self.USING_THREADS: 
                    task_executors.append(self.executor.submit(self.extract, component))
                else:
                    self.extract(component)
                ...
            
            wait(task_executors)


    def paged(self, url: str) -> None:

        while True:
            response: Response = self.api.get(url=url, headers=self.headers, max_retries=30)
            html = PyQuery(response.text)

            task_executors = []
            for card in self.collect_card(html):

                if '/folder/' in card:
                    ic(card)
                    self.paged(card)

                else:
                    component = (card, 0)

                    if self.USING_THREADS:
                        task_executors.append(self.executor.submit(self.extract, component))

                    else: 
                        self.extract(component)

                ...

            wait(task_executors)

            if not html.find('a.pagerNext').attr('href'): break
            url: str = self.main_url+html.find('a.pagerNext').attr('href')

        ...
        
    def main(self) -> None:

        match self.type_process:
            case 'one':
                component = (self.link, 0)
                self.extract(component)
                ...

            case 'page':
                self.paged(url=self.link)
                ...
        ...

        self.executor.shutdown(wait=True)
