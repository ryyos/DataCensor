
from requests import Response
from pyquery import PyQuery
from icecream import ic
from typing import List, Dict, Tuple

from library import BankmandiriLibs
from utils import *

class Bankmandiri(BankmandiriLibs):
    def __init__(self) -> None:
        super().__init__()
        ...

    def chef(self, datas: Tuple[List[Dict[str, any]]]) -> None:

        for type, data in zip(self.type, datas):
            path: str = self.base_path+type+'_bankmandiri.json'
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
        response: Response = self.api.get(self.target_url, headers=self.headers, cookies=self.cookies)
        html = PyQuery(response.text)

        direksi = html.find('div[data-analytics-asset-title="Direksi  main content"]')
        komisaris = html.find('div[data-analytics-asset-title="komisaris main content"]')

        results_direksi: List[dict] = []
        results_komesaris: List[dict] = []

        for direk, komi in zip(
            direksi.find('div[class="col-xs-6 col-sm-4 col-md-3"]'), 
            komisaris.find('div[class="col-xs-6 col-sm-4 col-md-3"]')):

            results_direksi.append(self.extract(PyQuery(direk)))
            results_komesaris.append(self.extract(PyQuery(komi)))
            ...

        self.chef((results_direksi, results_komesaris))
        ...