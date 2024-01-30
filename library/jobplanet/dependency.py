import json
import os
import json

from ApiRetrys import ApiRetry
from pyquery import PyQuery
from icecream import ic
from typing import List
from dotenv import load_dotenv

class JobPlanetLibs:
    def __init__(self) -> None:
        load_dotenv()
        self.api = ApiRetry(defaulth_headers=False, show_logs=True, handle_forbidden=True, redirect_url='https://id.jobplanet.com/')

        self.cookies = json.loads(os.getenv('JOBPLANET_COOKIES'))
        self.headers = json.loads(os.getenv('JOBPLANET_HEADER'))

        ...

    def collect_companies(self, url: str) -> List[str]:
        response = self.api.get(url=url, headers=self.headers, cookies=self.cookies)
        ic(response)

        html = PyQuery(response.text)

        companies = [PyQuery(companie).attr('href') for companie in html.find('dt[class="us_titb_l3"] a')]
        return companies
        ...

