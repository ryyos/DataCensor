
from requests import Response
from pyquery import PyQuery
from icecream import ic
from typing import List, Dict, Tuple

from library import BriLibs
from utils import *

class Bri(BriLibs):
    def __init__(self) -> None:
        super().__init__()
        ...

    def chef(self, datas: Tuple[List[Dict[str, any]]]) -> None:

        for index, data in enumerate(datas):
            path: str = self.base_path+self.type[index]+'_bri.json'
            result = {
                "link": self.target_url,
                "type": self.type[index],
                "domain": self.domain,
                "tags": [self.domain],
                "crawling_time": now(),
                "crawling_time_epoch": epoch(),
                "path_data_raw": self.base_path_s3+path,
                "path_data_clean": self.base_path_s3+convert_path(path),
                "datas": data
            }

            File.write_json(path, result)

            self.s3.upload(
                key=path,
                body=result,
                bucket=self.bucket
            )

        ...

    def main(self) -> None:
        response: Response = self.api.get(self.target_url)
        html = PyQuery(response.text)

        direksi: List[Dict[str, str]] = []
        komisaris: List[Dict[str, str]] = []

        for index, person in enumerate(html.find('section[class="section-manajemen manajemen"] > div[class="CX-modal hidden"]')):

            id: str = PyQuery(person).attr('id')

            resuls: Dict[str, str] = self.direksi(avatar=PyQuery(html.find('div[class="cx-tab-content"] div.img')[index]), 
                                                  bio=html.find('#'+id))
            
            if 'direksi' in id.lower():
                direksi.append(resuls)

            elif 'komisaris' in id.lower():
                komisaris.append(resuls)

        self.chef((direksi, komisaris))
        ...