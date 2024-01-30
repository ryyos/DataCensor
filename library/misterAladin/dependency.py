import os

from requests import Response
from ApiRetrys import ApiRetry
from pyquery import PyQuery
from typing import List
from icecream import ic

from utils import *

class MisterAladinLibs:
    def __init__(self) -> None:

        self.API_HOTELS = 'https://www.misteraladin.com/api/hotels/searches'
        self.api = ApiRetry(show_logs=True, defaulth_headers=True, redirect_url='https://www.misteraladin.com/')
        ...

    def buld_payload(self, page: int) -> dict[str, any]:
        return {
          "filter": {
            "check_in": "2024-01-30",
            "night": 1,
            "occupancy": 2,
            "room_quantity": 1,
            "city_id": "14"
          },
          "perpage": 50,
          "page": 1
        }
        
    def collect_hotels(self, url: str) -> List[str]:
        response: Response = self.api.get(url)
        html = PyQuery(response.text)

        hotels = [PyQuery(hotel).attr('href') for hotel in html.find('article[class="card-hotel default"] a')]
        return hotels
        ...