import os

from typing import List
from icecream import ic
from ApiRetrys import ApiRetry
from utils import *

class GofoodLibs:
    def __init__(self) -> None:
        self.__api = ApiRetry(show_logs=True, handle_forbidden=True, redirect_url='https://gofood.co.id')
        ...


    def create_dir(self, raw_data: dict) -> str:
        try: os.makedirs(f'data/data_raw/data_review/gofood/{raw_data["location_review"]}/{raw_data["location_restaurant"]["area"]}/{vname(raw_data["reviews_name"].lower())}/json')
        except Exception: ...
        finally: return f'data/data_raw/data_review/gofood/{raw_data["location_review"]}/{raw_data["location_restaurant"]["area"]}/{vname(raw_data["reviews_name"].lower())}/json'
        ...

    def collect_cities(self, url: str) -> List[str]:
        response = self.__api.get(url=url)

        return response.json()["pageProps"]["contents"][0]["data"]
        ...
        
    def buld_payload(self, page: str, latitude: float, longitude: float) -> dict:
        return {
            "code": "NEAR_ME",
            "country_code": "ID",
            "language": "id",
            "location": {
                "latitude": latitude,
                "longitude": longitude
            },
            "pageSize": 12,
            "pageToken": str(page),
            "timezone": "Asia/Jakarta"
        }
        ...

    def collect_card_restaurant(self, restaurant: str) -> List[str]:

        ic(restaurant)
        response = self.__retry(url=f'https://gofood.co.id/_next/data/{self.VERSION}/id{restaurant}/near_me.json?service_area={restaurant.split("/")[1]}&locality={restaurant.split("/")[-1]}&category=near_me')
            
        logger.info('fetch card food')

        latitude = response.json()["pageProps"]["userLocation"]["chosenLocation"]["latitude"]
        longitude = response.json()["pageProps"]["userLocation"]["chosenLocation"]["longitude"]

        page_token = 1
        cards = [card["path"] for card in response.json()["pageProps"]["outlets"]] # "/manado/restaurant/martabak-mas-narto-indomaret-a906c98d-2d31-48bc-8408-82dc1350cdca"
        while True:

            response = self.__retry(url=self.FOODS_API, 
                                    action='post',
                                    payload=self.__buld_payload(page=page_token, 
                                                              latitude=latitude,
                                                              longitude=longitude
                                                              ))

            ic(response)
            ic(self.uld_payload(page=page_token, 
                                    latitude=latitude,
                                    longitude=longitude
                                    ))
            if response.status_code != 200: break


            """ __create_card()

            Param:
                city   = | restaurant (/ketapang/restaurants) -> split("/")[1] -> ketapang
                pieces = | key "tenants/gofood/outlets/816ed6cd-72bf-4e10-9e50-37ce4d83e016" & displayName "Pempek Bang Awie, Wenang"

            Return:
                str: /ketapang/restaurant/pempek-bang-awie-wenang-a906c98d-2d31-48bc-8408-82dc1350cdca
            
            """
            card = [self.__create_card(city=restaurant.split("/")[1], pieces=card) for card in response.json()["outlets"]]
            cards.extend(card)

            
            logger.info(f'card page: {page_token}')
            logger.info(f'total card: {len(cards)}')
            print()

            try:
                page_token = response.json()["nextPageToken"]
                ic(response.json()["nextPageToken"])
                if page_token == '': break

            except Exception as err:
                ic(err)
                break

        return cards
        ...