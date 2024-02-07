import os

from requests import Response
from ApiRetrys import ApiRetry
from dekimashita import Dekimashita
from pyquery import PyQuery
from server.s3 import ConnectionS3
from dotenv import load_dotenv
from typing import List
from icecream import ic

from utils import *

class MisterAladinLibs:
        
    def __init__(self) -> None:
        load_dotenv()

        self.API_HOTELS = 'https://www.misteraladin.com/api/hotels/searches'
        self.API_TOURIST = 'https://www.misteraladin.com/api/generals/poi/nearby'
        self.API_DETAIL = 'https://www.misteraladin.com/api/hotel-review/review/hotel/328473?sort=newest&page=1&perpage=10'
        self.API_ROOM = 'https://www.misteraladin.com/api/hotels/v2/627676/availability?check_in=2024-01-30&night=1&occupancy=2&room_quantity=1&lang=id'
        self.MAIN_URL = 'https://www.misteraladin.com'
        self.API_REVIEW = 'https://www.misteraladin.com/api/hotel-review/review/hotel/'
        self.DOMAIN = 'www.misteraladin.com'

        self.api = ApiRetry(show_logs=True, defaulth_headers=True, redirect_url=self.MAIN_URL, handle_forbidden=True)

        self.s3 = ConnectionS3(access_key_id=os.getenv('ACCESS_KEY_ID'),
                                 secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
                                 endpoint_url=os.getenv('ENDPOINT'),
                                 )

        self.logs = Logs(path_monitoring='logs/misteraladin/monitoring_data.json',
                            path_log='logs/misteraladin/monitoring_logs.json',
                            domain='www.misteraladin.com')
        
        self.bucket = os.getenv('BUCKET')
        ...

    def build_payload(self, page: int, city_id: int) -> dict[str, any]:
        return {
          "filter": {
            "check_in": today(),
            "night": 1,
            "occupancy": 2,
            "room_quantity": 1,
            "city_id": str(city_id)
          },
          "perpage": 50,
          "page": page
        }

    def collect_hotels(self, city_id: int, page: int) -> List[dict[str, any]]:
        response: Response = self.api.post(url=self.API_HOTELS, json=self.build_payload(page, city_id))
        if response.json()['data']: return response.json()['data']
        else: return None
        ...

    def build_url(self, hotel: dict) -> str:
        # https://www.misteraladin.com/hotel/indonesia/jakarta/mangga-besar/luminor-hotel-kota/328473?
        return f'{self.MAIN_URL}/hotel/{hotel["area"]["city"]["state"]["country"]["slug"]}/{hotel["area"]["city"]["slug"]}/{hotel["area"]["slug"]}/{hotel["slug"]}/{hotel["id"]}'
        ...

    def build_param_review(self, page: int) -> dict[str, str]:
        return {
            "sort": "newest",
            "page": str(page),
            "perpage": "10"
        }

    def build_param_tourist(self, hotel: dict) -> dict[str, str]:
        return {
            "lat": hotel["latitude"],
            "long": hotel["longitude"],
            "is_active": "1",
            "include": "type.icon"
        }
        ...

    def build_param_room(self) -> dict[str, str]:
        return {
            "check_in": str(today()),
            "night": "2",
            "occupancy": "2",
            "room_quantity": "1",
            "lang": "id"
        }
        ...

    def tourist_attraction(self, hotel: dict) -> List[dict]:
        # https://www.misteraladin.com/api/generals/poi/nearby?lat=-6.184711&long=106.831482&is_active=1&include=type.icon
        response: Response = self.api.get(url=self.API_TOURIST, params=self.build_param_tourist(hotel))

        return [
            {
                "address": place["address"],
                "distance": place["distance"],
                "active": place["is_active"],
                "popular": place["is_popular"],
                "name": place["name"],
                "type": place.get("type", {}).get("name_en", None) if place.get("type") else None
            } for place in response.json()["data"]
        ]
        ...

    def set_descriptions(self, html) -> str:
        try: return html.find('script').text().split('description:"')[1].split('"')[0]
        except Exception: return None
        ...

    def available_rooms(self, hotel: dict) -> List[str]:
        response: Response = self.api.get(url=f'https://www.misteraladin.com/api/hotels/v2/{hotel["id"]}/availability',
                                          params=self.build_param_room())
        rooms: List[dict] = []
        for room in response.json()["data"]: 
            rooms.append(Dekimashita.vdict(room, ['\n', '\r']))

        return rooms
        ...

    def get_detail_hotel(self, id: int) -> dict:
        response: Response = self.api.get()
        ...

    def create_dir(self, headers: dict) -> str:
        try: os.makedirs(f'data/data_raw/data_review/mister_aladin/{headers["country"]}/{headers["city"]}/{headers["subdistrict"]}/{Dekimashita.vdir(headers["reviews_name"])}/json/detail')
        except Exception: ...
        finally: return f'data/data_raw/data_review/mister_aladin/{headers["country"]}/{headers["city"]}/{headers["subdistrict"]}/{Dekimashita.vdir(headers["reviews_name"])}/json'
        ...