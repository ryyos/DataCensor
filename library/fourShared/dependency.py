import os

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

    def extract_navbar(self, html: PyQuery) -> Tuple[str]:
        (size, posted, types, _) = html.find('p.fileInfo').text().split(' |')

        return (' '.join(size.split(' ')[1:]), posted.strip(), types.strip())
        ...

    def create_dir(self, title: str) -> str:

        format = title.split('.')[-1]
        path = f'data/data_raw/admiralty/four_shared/{format}/{Dekimashita.vdir(title)}.{format}'
        
        try:
            if self.SAVE_TO_LOKAL: os.makedirs(path)
        except Exception: ...
        finally: return path
        ...

    def collect_document(self, url: str) -> List[str]:
        response: Response = self.api.get(url=url, headers=self.headers, cookies=self.cookies)
        html = PyQuery(response.text)

        return [PyQuery(url).attr('href') for url in html.find('a[target="_top"]')]
        ...

    


# data/admiralty/four_shared/json/title.json
# data/admiralty/four_shared/pdf/file.pdf