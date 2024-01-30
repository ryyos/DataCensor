
from ApiRetrys import ApiRetry
from requests import Response
from pyquery import PyQuery
from library import JobPlanetLibs
from time import time
from icecream import ic
from utils import *

class JobPlanet:
    def __init__(self) -> None:

        self.__jobplanet = JobPlanetLibs()

        self.MAIN_URL = 'https://id.jobplanet.com'
        self.DOMAIN = 'id.jobplanet.com'

        ...

    def get_detail(self, url: str) -> dict[str, any]:
        response: Response = self.__jobplanet.api.get(url=url, headers=self.__jobplanet.headers, cookies=self.__jobplanet.cookies)
        ic(response)
        ic(response.text)
        html = PyQuery(response.text)

        headers = {
            "link": url,
            "domain": self.DOMAIN,
            "tag": ["id.jobplanet.com"],
            "crawling_time": now(),
            "crawling_time_epoch": int(time()),
            "path_data_raw": "",
            "path_data_clean": "",
            "reviews_name": html.find('h1[class="tit"]').text(),
            "location_reviews": None,
            "category_reviews": None,

            "total_reviews": html.find('h2[class="stats_ttl"]').text(),
            "reviews_rating": {
              "total_rating": html.find('span[class="icon star"]').text(),
              "detail_total_rating": [
                {
                  "score_rating": html.find(f'dl[class="rate_bar_set"] dd:nth-child({dd+1})'),
                  "category_rating": PyQuery(dt).text()
                } for dd, dt in html.find('dl[class="rate_bar_set"] dt')
              ]
            }
        }

        ic(headers)
        ...

    def main(self) -> None:

        page = 1
        while True:
            companies = self.__jobplanet.collect_companies(f'https://id.jobplanet.com/companies/?page={page}')

            for companie in companies:

                headers = self.get_detail(self.MAIN_URL+companie)

                break
                ...

            page+=1
            break

        ...