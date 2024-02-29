
from requests import Response
from pyquery import PyQuery
from typing import Dict, List, Tuple
from icecream import ic

from library import DanamonLibs
from utils import *

class Danamon(DanamonLibs):
    def __init__(self) -> None:
        super().__init__()

        ...
    def chef(self, datas: Tuple[List[Dict[str, any]]]) -> None:

        for type, data in zip(self.type, datas):
            path: str = self.base_path+type+'_danamon.json'
            result = {
                "link": self.target_url,
                "type": type,
                "domain": self.domain,
                "tags": [self.domain],
                "crawling_time": now(),
                "crawling_time_epoch": epoch(),
                "path_data_raw": self.base_path_s3+path,
                "path_data_clean": self.base_path_s3+convert_path(path),
                "datas": data
            }

            File.write_json(path, result)

            # self.s3.upload(
            #     key=path,
            #     body=result,
            #     bucket=self.bucket
            # )


    def main(self) -> None:
        response: Response = self.api.get(self.target_url)
        html = PyQuery(response.text)

        File.write_str('private/nodamon.html', response.text)

        all_direksi: List[str] = html.find('#sidebar > ul > li:nth-child(2) > ul > li')
        all_komisaris: List[str] = html.find('#sidebar > ul > li:nth-child(1) > ul > li')

        results_direksi: List[dict] = []
        results_komisaris: List[dict] = []

        for direksi in all_direksi:
            results_direksi.append(self.extract(self.base_url+PyQuery(direksi).find('a').attr('href')))

        for komisaris in all_komisaris:
            results_komisaris.append(self.extract(self.base_url+PyQuery(komisaris).find('a').attr('href')))
            ...

        self.chef((results_direksi, results_komisaris))
        ...


# "data/data_raw/admiralty/data_perbankan/danamon"