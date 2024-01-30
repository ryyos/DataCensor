import os

from typing import List
from icecream import ic
from ApiRetrys import ApiRetry

from component import codes
from utils import *

class GofoodLibs:
    def __init__(self) -> None:
        self.__api = ApiRetry(show_logs=True, handle_forbidden=True, redirect_url='https://gofood.co.id', defaulth_headers=True)

        self.VERSION = '9.0.1'
        self.FOODS_API = f'https://gofood.co.id/api/outlets'
        self.API_REVIEW_PAGE = 'https://gofood.co.id/api/outlets/'
        ...


    def create_dir(self, raw_data: dict) -> str:
        try: os.makedirs(f'data/data_raw/data_review/gofood/{raw_data["location_review"]}/{raw_data["location_restaurant"]["area"]}/{Dekimashita.vname(raw_data["reviews_name"].lower())}/json/detail')
        except Exception: ...
        finally: return f'data/data_raw/data_review/gofood/{raw_data["location_review"]}/{raw_data["location_restaurant"]["area"]}/{Dekimashita.vname(raw_data["reviews_name"].lower())}/json'
        ...

    def collect_cities(self, url: str) -> List[str]:
        response = self.__api.get(url=url)

        return response.json()["pageProps"]["contents"][0]["data"]
        ...
        
    def create_card(self, city: str, pieces: dict) -> str:
        return f'/{city}/restaurant/{Dekimashita.vname(pieces["core"]["displayName"].lower()).replace("--", "-")}-{pieces["core"]["key"].split("/")[-1]}'
        ...

    def write_detail(self, headers: dict):
        headers["reviews_name"] = headers["reviews_name"]
        ic(headers["reviews_name"])

        path_detail = f'{self.create_dir(raw_data=headers)}/detail/{Dekimashita.vname(headers["reviews_name"])}.json'

        headers.update({
            "path_data_raw": 'S3://ai-pipeline-statistics/'+path_detail,
            "path_data_clean": 'S3://ai-pipeline-statistics/'+convert_path(path_detail)
        })

        File.write_json(path_detail, headers)
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

        ic(restaurant)
        response = self.__api.get(url=f'https://gofood.co.id/_next/data/{self.VERSION}/id{restaurant}/near_me.json?service_area={restaurant.split("/")[1]}&locality={restaurant.split("/")[-1]}&category=near_me', max_retries=30)
            
        logger.info('fetch card food')

        latitude = response.json()["pageProps"]["userLocation"]["chosenLocation"]["latitude"]
        longitude = response.json()["pageProps"]["userLocation"]["chosenLocation"]["longitude"]

        page_token = 1
        cards = [card["path"] for card in response.json()["pageProps"]["outlets"]] # "/manado/restaurant/martabak-mas-narto-indomaret-a906c98d-2d31-48bc-8408-82dc1350cdca"
        while True:

            response = self.__api.post(url=self.FOODS_API,
                                    json=self.buld_payload(page=page_token, 
                                                              latitude=latitude,
                                                              longitude=longitude
                                                              ))

            ic(response)
            ic(self.buld_payload(page=page_token, 
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

        ic(len(cards))
        return cards
        ...

    def collect_reviews(self, headers: dict) -> List[dict]:
        uid = headers["restaurant_id"]
        page = '?page=1&page_size=50'
        
        response = self.__api.get(url=f'{self.API_REVIEW_PAGE}{uid}/reviews{page}',max_retries=30)

        ic(response)
        ...
        all_reviews: List[dict] = []
        error: List[dict] = []
        
        if response.status_code == 200:
            page_review = 1
            while True:

                reviews = response.json()["data"]
                for review in reviews: all_reviews.append(review)

                logger.info(f'page review: {page_review}')
                logger.info(f'api review page: {self.API_REVIEW_PAGE}{uid}/reviews{page}')
                print()

                page = response.json().get("next_page", None)
                if page:
                    ic(page)
                    response = self.__api.get(url=f'{self.API_REVIEW_PAGE}{uid}/reviews{page}', max_retries=30)

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