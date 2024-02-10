import requests
from urllib import request

from requests import Response
from pyquery import PyQuery
from typing import Dict, Tuple
from library import FourSharedLibs
from dekimashita import Dekimashita
from concurrent.futures import wait
from time import sleep

from utils import *

class FourShared(FourSharedLibs):
    def __init__(self, save: bool, s3: bool, thread: bool) -> None:
        super().__init__(save)
        self.update_cookies()

        self.SAVE_TO_S3 = s3
        self.SAVE_TO_LOKAL = save
        self.USING_THREADS = thread
        ...

    def extract(self, component: Tuple[str]) -> None:
        (url, item) = component

        response: Response = self.api.get(url=url)
        html = PyQuery(response.text)

        title = html.find('h1.fileName').text()
        if not title:
            title = html.find('div[class="generalFilename"]').text()

        path = f'{self.create_dir(format="json")}/{title.split(".")[0].replace(" ", "_")}.json'

        (size, posted, types) = self.extract_navbar(html)

        name_documents = None
        try:
            (name_documents, url_documents) = self.collect_document(html.find('#moreFilesIFrame').attr('src'))
        except Exception: ...

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

        File.write_json(path, headers)

        if not item:

            task_executors = []
            for index, url in enumerate(url_documents):
                
                component = (url, index+1)

                if self.USING_THREADS: 
                    task_executors.append(self.executor.submit(self.extract, component))
                else:
                    self.extract(component)
                ...
            
            wait(task_executors)

        ...
    
    def main(self) -> None:
        component = (self.link, 0)

        self.extract(component)
        self.executor.shutdown(wait=True)


        ...



