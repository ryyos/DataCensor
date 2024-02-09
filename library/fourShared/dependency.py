import os
import requests

from time import sleep
from typing import Dict, Tuple, List
from ApiRetrys import ApiRetry
from requests import Response
from pyquery import PyQuery
from concurrent.futures import ThreadPoolExecutor
from icecream import ic
from dekimashita import Dekimashita

from components import FourSharedAsset
from utils import *

class FourSharedLibs(FourSharedAsset):
    def __init__(self, save: bool) -> None:
        super().__init__()

        self.api = ApiRetry(show_logs=True)
        self.executor = ThreadPoolExecutor()

        self.SAVE_TO_LOKAL = save

        ...

    def extract_navbar(self, html: PyQuery) -> Tuple[str]:
        (size, posted, types, _) = html.find('p.fileInfo').text().split(' |')

        return (' '.join(size.split(' ')[1:]), posted.strip(), types.strip())
        ...

    def create_dir(self, format: str) -> str:
        path = f'data/data_raw/admiralty/four_shared/{format}'
        try:
            if self.SAVE_TO_LOKAL: os.makedirs(path)
        except Exception: ...
        finally: return path
        ...

    def collect_document(self, url: str) -> List[str]:
        response: Response = self.api.get(url='https:'+url)
        html = PyQuery(response.text)

        names: List[str] = []
        urls: List[str] = []

        for url in html.find('a[target="_top"]'):
            urls.append(PyQuery(url).attr('href'))
            names.append(PyQuery(url).text())

        return (names, urls)
        ...

    def download(self, html: PyQuery, header: Dict[str, any]) -> Dict[str, any]:

        url = html.find('#btnLink').attr('href')
        response = self.api.get(url)
        html = PyQuery(response.text)

        url_document: str = html.find('input[name="d3link"]').attr('value')
        
        response = requests.get(url=url_document, 
                                cookies=self.cookies, 
                                headers=self.headers)
        
        sleep(20)
        
        response = requests.get(url=url_document, 
                                cookies=self.cookies, 
                                headers=self.headers)

        path_document = f'{self.create_dir(url_document.split("?")[0].split(".")[-1])}/{header["detail"]["title"].split(".")[0].replace(" ", "_")}.{url_document.split("?")[0].split(".")[-1]}'
        ic(response.headers)
        ic(url_document)
        ic(path_document)
        header.update({
            "path_data_document": path_document
        })
        
        with open(path_document, 'wb') as f:
            f.write(response.content)

        return header
        ...


    


# data/admiralty/four_shared/json/title.json
# data/admiralty/four_shared/pdf/file.pdf