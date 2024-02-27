
from requests import Response
from concurrent.futures import ThreadPoolExecutor, wait
from pyquery import PyQuery
from typing import List, Dict

from library import ArchiveLibs
from utils import *

class Archive(ArchiveLibs):
    def __init__(self, url: str, s3: bool, save: bool, types: str, threads: bool) -> None:
        super().__init__(save, s3, threads)

        self.SAVE_TO_S3: bool = s3
        self.SAVE_TO_LOKAL: bool = save
        self.target_url: str = url
        self.type: str = types

    def book(self, url: str) -> None:
        response: Response = self.api.get(url)
        html = PyQuery(response.text)

        (url_page, id) = self.url_download_page(html)

        documents: List[dict] = self.collect_documents(url_page)
        
        headers = {
            "id": id,
            "link": url,
            "domain": self.domain,
            "tag": [self.domain],
            "crawling_time": now(),
            "crawling_time_epoch": epoch(),
            "path_data_raw": "",
            "path_data_clean": "",
            "documents": documents
        }

        headers: dict = self.download(headers)

        if self.SAVE_TO_LOKAL:
            File.write_json(headers["path_data_raw"].replace(self.s3_path, ''), content=headers)

        if self.SAVE_TO_S3:
            self.s3.upload(
                key=headers["path_data_raw"].replace(self.s3_path, ''),
                body=headers,
                bucket=self.bucket
            )
        ...

    def main(self) -> None:

        match self.type:
            case 'book':
                self.book(self.target_url)
                ...

            case 'page':
                self.get_name_page(self.target_url)
                for card in self.collect_card(self.target_url):
                    self.book(card)
                ...
                
        self.executor.shutdown(wait=True)
        ...