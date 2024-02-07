import os

from typing import List
from icecream import ic
from ApiRetrys import ApiRetry
from dekimashita import Dekimashita
from server.s3 import ConnectionS3
from components import codes
from dotenv import load_dotenv
from utils import *

class GofoodLibs:
    def __init__(self, save: bool) -> None:
        load_dotenv()
        self.api = ApiRetry(show_logs=True, handle_forbidden=True, redirect_url='https://gofood.co.id', defaulth_headers=True)

        self.s3 = ConnectionS3(access_key_id=os.getenv('ACCESS_KEY_ID'),
                                 secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
                                 endpoint_url=os.getenv('ENDPOINT'),
                                 )


        self.logs = Logs(path_monitoring='logs/gofood/monitoring_data.json',
                            path_log='logs/gofood/monitoring_logs.json',
                            domain='gofood.co.id')

        self.SAVE_TO_LOKAL = save

        self.bucket = os.getenv('BUCKET')
        self.VERSION = '9.0.2'
        self.FOODS_API = f'https://gofood.co.id/api/outlets'
        self.API_REVIEW_PAGE = 'https://gofood.co.id/api/outlets/'
        ...


    def create_dir(self, raw_data: dict, create: bool) -> str:
        try: 
            if create: os.makedirs(f'data/data_raw/data_review/gofood/{raw_data["location_review"]}/{raw_data["location_restaurant"]["area"]}/{Dekimashita.vdir(raw_data["reviews_name"])}/json/detail')
        except Exception: ...
        finally: return f'data/data_raw/data_review/gofood/{raw_data["location_review"]}/{raw_data["location_restaurant"]["area"]}/{Dekimashita.vdir(raw_data["reviews_name"])}/json'
        ...

    def collect_cities(self, url: str) -> List[str]:
        response = self.api.get(url=url)

        return response.json()["pageProps"]["contents"][0]["data"]
        ...
        
    def create_card(self, city: str, pieces: dict) -> str:
        return f'/{city}/restaurant/{Dekimashita.vdir(pieces["core"]["displayName"], "-")}-{pieces["core"]["key"].split("/")[-1]}'
        ...

    def write_detail(self, headers: dict):
        headers["reviews_name"] = headers["reviews_name"]
        path_detail = f'{self.create_dir(raw_data=headers, create=self.SAVE_TO_LOKAL)}/detail/{Dekimashita.vdir(headers["reviews_name"])}.json'

        headers.update({
            "path_data_raw": 'S3://ai-pipeline-statistics/'+path_detail,
            "path_data_clean": 'S3://ai-pipeline-statistics/'+convert_path(path_detail)
        })

        return {
            "path_detail": path_detail,
            "data_detail": headers
        }
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

        response = self.api.get(url=f'https://gofood.co.id/_next/data/{self.VERSION}/id{restaurant}/near_me.json?service_area={restaurant.split("/")[1]}&locality={restaurant.split("/")[-1]}&category=near_me', max_retries=30)

        latitude = response.json()["pageProps"]["userLocation"]["chosenLocation"]["latitude"]
        longitude = response.json()["pageProps"]["userLocation"]["chosenLocation"]["longitude"]

        page_token = 1
        cards = [card["path"] for card in response.json()["pageProps"]["outlets"]] # "/manado/restaurant/martabak-mas-narto-indomaret-a906c98d-2d31-48bc-8408-82dc1350cdca"
        while True:

            response = self.api.post(url=self.FOODS_API,
                                    json=self.buld_payload(page=page_token, 
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
            card = [self.create_card(city=restaurant.split("/")[1], pieces=card) for card in response.json()["outlets"]]
            cards.extend(card)

            
            Runtime.cards(restaurant, 'card', page_token, len(cards))

            try:
                page_token = response.json()["nextPageToken"]
                if page_token == '': break

            except Exception as err:
                ic(err)
                break

        return cards
        ...

    def collect_reviews(self, headers: dict) -> List[dict]:
        uid = headers["restaurant_id"]
        page = '?page=1&page_size=50'
        
        response = self.api.get(url=f'{self.API_REVIEW_PAGE}{uid}/reviews{page}',max_retries=30)
        ...
        all_reviews: List[dict] = []
        error: List[dict] = []
        
        if response.status_code == 200:
            page_review = 1
            while True:

                reviews = response.json()["data"]
                for review in reviews: all_reviews.append(review)

                Runtime.cards(uid, 'review', page_review, len(all_reviews))

                page = response.json().get("next_page", None)
                if page:
                    response = self.api.get(url=f'{self.API_REVIEW_PAGE}{uid}/reviews{page}', max_retries=30)

                    ... # Jika gagal request ke  review page selanjutnya
                    if response.status_code != 200: 
                        error.append({
                            "message": response.text,
                            "type": codes[str(response.status_code)],
                            "id": None
                        })
                        break

                    ...
                    page_review+=1

                else: break


        else:
            ... # Jika gagal request di review pertama
            error.append({
                "message": response.text,
                "type": codes[str(response.status_code)],
                "id": None
            })

        return {
            "all_reviews": all_reviews,
            "error": error
        }

        ...