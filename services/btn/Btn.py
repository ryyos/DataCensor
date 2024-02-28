
from pyquery import PyQuery
from requests import Response
from typing import List, Dict, Tuple
from icecream import ic

from library import BtnLibs
from utils import *

class Btn(BtnLibs):
    def __init__(self) -> None:
        super().__init__()
        ...

    def chef(self, datas: Tuple[List[Dict[str, any]]]) -> None:

        for type, data in zip(self.type, datas):
            path: str = self.base_path+type+'_btn.json'
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
        response: Response = self.api.get(self.target_url, headers=self.headers, cookies=self.cookies)
        html = PyQuery(response.text)

        all_direksi = html.find('#tabe2946505-ec37-44f8-b52b-bc66ee448973_1 div.detail-profile-box ')
        all_komisaris = html.find('#tabe2946505-ec37-44f8-b52b-bc66ee448973_0 div.detail-profile-box ')

        results_direksi: List[dict] = []
        results_komesaris: List[dict] = []

        for direksi, komisaris in zip(all_direksi, all_komisaris):
            results_direksi.append(self.extract(PyQuery(direksi)))
            results_komesaris.append(self.extract(PyQuery(komisaris)))
            ...

        self.chef((results_direksi, results_komesaris))
        ...