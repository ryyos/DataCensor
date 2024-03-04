
from typing import List, Dict, Tuple
from requests import Response
from pyquery import PyQuery
from icecream import ic

from library import BcaLibs
from utils import *

class Bca(BcaLibs):
    def __init__(self) -> None:
        super().__init__()
        ...

    def chef(self, datas: Tuple[List[Dict[str, any]]]) -> None:

        for type, data in zip(self.type, datas):
            path: str = self.base_path+type+'_bca.json'
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

            self.s3.upload(
                key=path,
                body=result,
                bucket=self.bucket
            )

    def main(self) -> None:
        response: Response = self.api.get(self.target_url)
        html = PyQuery(response.text)

        
        raw_direksi = html.find('div.container.my-48 > div > div:nth-child(4)')
        raw_komesaris = html.find('div.container.my-48 > div > div:nth-child(2)')

        results_direksi: List[dict] = []
        results_komesaris: List[dict] = []

        for direksi in raw_direksi.find('div.a-card a'):
            try:
                results_direksi.append(self.extract(self.base_url+PyQuery(direksi).attr('href'), 'direksi'))

            except Exception as err:
                ic(err)

        for komesaris in raw_komesaris.find('div.a-card a'):
            try:
                results_komesaris.append(self.extract(self.base_url+PyQuery(komesaris).attr('href'), 'komesaris'))

            except Exception as err:
                ic(err)

        self.chef((results_direksi, results_komesaris))

        ...
        # "data/data_raw/admiralty/data_perbankan/bca"