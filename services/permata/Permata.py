
from requests import Response
from pyquery import PyQuery
from typing import Dict, List, Tuple
from icecream import ic

from library import  PermataLibs
from utils import *

class Permata(PermataLibs):
    def __init__(self) -> None:
        super().__init__()
        ...

    def chef(self, datas: Tuple[List[Dict[str, any]]]) -> None:

        for type, data in zip(self.type, datas):
            path: str = self.base_path+type+'_permatabank.json'
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

        all_direksi = html.find('section[data-id="Direksi"]')
        all_komesaris = html.find('section[data-id="Dewan-Komisaris"]')

        results_direksi: List[str] = []
        results_komisaris: List[str] = []

        for direksi, komesaris in zip(all_direksi.find('div.card-item'), all_komesaris.find('div.card-item')):
            results_direksi.append(self.extract(PyQuery(direksi)))
            results_komisaris.append(self.extract(PyQuery(komesaris)))
            ...


        self.chef((results_direksi, results_komisaris))
        ...

        # "data/data_raw/admiralty/data_perbankan/permatabank"