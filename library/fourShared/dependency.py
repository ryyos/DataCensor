
from typing import Dict, Tuple
from ApiRetrys import ApiRetry
from requests import Response
from pyquery import PyQuery
from icecream import ic

from components import FourSharedAsset
from utils import *

class FourSharedLibs(FourSharedAsset):
    def __init__(self) -> None:
        super().__init__()

        self.api = ApiRetry(show_logs=True)

    def extract_navbar(self, html: PyQuery) -> Tuple[str]:
        (size, posted, types, _) = html.find('p.fileInfo').text().split(' |')

        return (' '.join(size.split(' ')[1:]), posted.strip(), types.strip())
        ...


    def extract_header(self, url: str) -> Dict[str, any]:
        response: Response = self.api.get(url=url, headers=self.headers, cookies=self.cookies)
        html = PyQuery(response.text)

        (size, posted, types) = self.extract_navbar(html)

        headers = {
            "link": self.link,
            "domain": self.domain,
            "tag": [PyQuery(tag).text() for tag in html.find('#tagsDiv a')],
            "crawling_time": now(),
            "crawling_time_epoch": epoch(),
            "path_data_raw": "string",
            "path_data_clean": "string",
            "detail": {
                "title": html.find('h1.fileName').text(),
                "owner": html.find('a.fileOwner').text(),
                "size": size,
                "posted": posted,
                "type": types,
                "description": html.find('#fileDescriptionText').text()
            }
        }

        ic(headers)
        ...
    


# data/admiralty/four_shared/json/title.json
# data/admiralty/four_shared/pdf/file.pdf