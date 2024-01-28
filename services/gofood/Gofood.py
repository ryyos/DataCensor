import os
import datetime as date
import requests
import json

from zlib import crc32
from requests import Session
from time import time, sleep, strftime
from datetime import datetime, timezone
from icecream import ic
from tqdm import tqdm
from fake_useragent import FakeUserAgent
from typing import List
from ApiRetrys import ApiRetry
from dotenv import *

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait

from server.s3 import ConnectionS3
from library import GofoodLibs
from utils import *

class Gofood:
    def __init__(self) -> None:
        load_dotenv()

        self.__api = ApiRetry(defaulth_headers=True, show_logs=True, handle_forbidden=True, redirect_url='https://gofood.co.id')

        self.__file = File()
        self.__gofood = GofoodLibs()
        self.__sessions = Session()
        self.__executor = ThreadPoolExecutor()
        self.__char: str = []

        self.__s3 = ConnectionS3(access_key_id=os.getenv('ACCESS_KEY_ID'),
                                 secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
                                 endpoint_url=os.getenv('ENDPOINT'),
                                 )


        self.__logs = Logs(path_monitoring='logs/gofood/monitoring_data.json',
                            path_log='logs/gofood/monitoring_logs.json',
                            domain='gofood.co.id')
        

        self._bucket = os.getenv('BUCKET')
        self.__datas: List[dict] = []
        self.__monitorings: List[dict] = []

        self.VERSION = '9.0.0'

        self.DOMAIN = 'gofood.co.id'
        self.MAIN_URL = 'https://gofood.co.id'
        self.MAIN_PATH = 'data'
        self.LOG_PATH_SUC = 'logs/results.txt'
        self.LOG_PATH_ERR = 'logs/detail.txt'
        self.PIC = 'Rio Dwi Saputra'

        self.API_CITY = f'https://gofood.co.id/_next/data/{self.VERSION}/id/cities.json' # 89
        self.RESTAURANT = f'https://gofood.co.id/_next/data/{self.VERSION}/id/jakarta/restaurants.json' # 94
        self.NEAR_ME_API = f'https://gofood.co.id/_next/data/{self.VERSION}/id/jakarta/bekasi-restaurants/near_me.json' 
        self.FOODS_API = f'https://gofood.co.id/api/outlets'
        self.API_REVIEW = f'https://gofood.co.id/_next/data/{self.VERSION}/id/jakarta/restaurant/mcdonald-s-pekayon-50150204-8f6d-4372-8458-668f1be126e8/reviews.json?id=mcdonald-s-pekayon-50150204-8f6d-4372-8458-668f1be126e8'
        self.API_REVIEW_PAGE = 'https://gofood.co.id/api/outlets/'

        self.PRICE = {
            '0': 'Not Set',
            '1': '<16k',
            '2': '16k-40k',
            '3': '40k-100k',
            '4': '>100k',
        }

        self.RATING = {
            "CANNED_RESPONSE_TASTE": "taste",
            "CANNED_RESPONSE_PORTION": "portion",
            "CANNED_RESPONSE_PACKAGING": "packaging",
            "CANNED_RESPONSE_FRESHNESS": "freshness",
            "CANNED_RESPONSE_VALUE": "prices",
            "CANNED_RESPONSE_HYGIENE": "hygiene",
        }



    def __get_review(self, raw_json: dict):

        logger.info('extract review from restaurant')
        uid = raw_json["restaurant_id"]
        
        details: dict = self.__gofood.write_detail(raw_json)

        # self.__s3.upload(key=details["path_detail"], body=details["data_detail"], bucket=self._bucket)
        File.write_json(path=details["path_detail"], content=details["data_detail"])

        reviews: dict = self.__gofood.collect_reviews(raw_json)
        raw_json["total_reviews"] = len(reviews["all_reviews"])

        ic(len(reviews["all_reviews"]))
        
        for index, comment in tqdm(enumerate(reviews["all_reviews"]), ascii=True, smoothing=0.1, total=len(reviews["all_reviews"])):
            detail_reviews = {
                "id_review": comment["id"],
                "username_reviews": comment["author"]["fullName"],
                "initialName": comment["author"]["initialName"],
                "image_reviews": comment["author"]["avatarUrl"],
                "created_time": comment["createdAt"].split('.')[0].replace('T', ' '),
                "created_time_epoch": convert_time(comment["createdAt"]),
                "email_reviews": None,
                "company_name": None,
                "location_reviews": None,
                "title_detail_reviews": None,
                "reviews_rating": comment["rating"],
                "detail_reviews_rating": [{
                    "score_rating": None,
                    "category_rating": None
                }],
                "total_likes_reviews": None,
                "total_dislikes_reviews": None,
                "total_reply_reviews": None,
                "orders": comment["order"],
                "tags_review": comment["tags"],
                "content_reviews": comment["text"],
                "reply_content_reviews": {
                    "username_reply_reviews": None,
                    "content_reviews": None
                },
                "date_of_experience": comment["createdAt"].split('.')[0].replace('T', ' '),
                "date_of_experience_epoch": convert_time(comment["createdAt"]),
            }

            path_data = self.__gofood.create_dir(raw_data=raw_json)

            detail_reviews["tags_review"].append(self.DOMAIN)

            raw_json.update({
                "detail_reviews": detail_reviews,
                "path_data_raw": f'S3://ai-pipeline-statistics/{path_data}/{detail_reviews["id_review"]}.json',
                "path_data_clean": f'S3://ai-pipeline-statistics/{convert_path(path_data)}/{detail_reviews["id_review"]}.json'
            })

            # response = self.__s3.upload(key=path_data, body=raw_json, bucket=self._bucket)
            response = 200
            if index in [2,5,6,4,9,6,11,12]: response = 404

            File.write_json(path=f'{path_data}/{detail_reviews["id_review"]}.json', content=raw_json)

            error = self.__logs.logsS3(func=self.__logs,
                               header=raw_json,
                               index=index,
                               response=response,
                               reviews=reviews)

            reviews["error"].extend(error)

        self.__logs.logsS3Err(func=self.__logs,
                              header=raw_json,
                              reviews=reviews)
        ...

    def __extract_restaurant(self, ingredient: dict):
            cards = self.__gofood.collect_card_restaurant(restaurant=ingredient["restaurant"]["path"]) # Mengambil card restaurant dari area

            ic(len(cards))
            for index, card in enumerate(cards):
                ic(card)


                """ api_review

                Param:
                    card | /ketapang/restaurant/pempek-bang-awie-wenang-a906c98d-2d31-48bc-8408-82dc1350cdca
                
                """
                api_review = f'https://gofood.co.id/_next/data/{self.VERSION}/id{card}/reviews.json?id={card.split("/")[-1]}'
                
            
                try:
                    food_review = self.__api.get(url=api_review, max_retries=30)
                    logger.info(card)

                    # Jika di redirect maka ambil destination dan request ke path yang di berikan
                    if food_review.json()["pageProps"].get("__N_REDIRECT", None):
                        ic('masuk redirect')
                        ic(food_review.json()["pageProps"]["__N_REDIRECT"])
                        food_review = self.__api.get(url=f'https://gofood.co.id/_next/data/{self.VERSION}/id{food_review.json()["pageProps"]["__N_REDIRECT"]}/reviews.json?id={card.split("/")[-1]}', max_retries=30)


                    header_required = {
                        "id": crc32(vname(food_review.json()["pageProps"]["outlet"]["core"]["displayName"]).encode('utf-8')),
                        "link": self.MAIN_URL+food_review.json()["pageProps"].get("outletUrl"),
                        "domain": self.DOMAIN,
                        "tags": [tag["displayName"] for tag in food_review.json()["pageProps"]["outlet"]["core"]["tags"]],
                        "crawling_time": strftime('%Y-%m-%d %H:%M:%S'),
                        "crawling_time_epoch": int(time()),
                        "path_data_raw": "",
                        "path_data_clean": "",
                        "reviews_name": food_review.json()["pageProps"]["outlet"]["core"]["displayName"],
                        "location_review": ingredient["city"]["name"].lower(),
                        "category_reviews": "food & baverage",
                        "total_reviews": 0,

                        "location_restaurant": {
                            "city": ingredient["city"]["name"].lower(),
                            "area": ingredient["restaurant"]["path"].split("/")[-1],
                            "distance_km": food_review.json()["pageProps"]["outlet"]["delivery"]["distanceKm"],
                        },

                        "range_prices": self.PRICE[str(food_review.json()["pageProps"]["outlet"]["priceLevel"])],
                        "restaurant_id": food_review.json()["pageProps"]["outlet"]["uid"],

                        "reviews_rating": {
                            "total_ratings": food_review.json()["pageProps"]["outlet"]["ratings"],
                            "detail_total_rating": [
                                {
                                    "category_rating": self.RATING[rating["id"]],
                                    "score_rating": rating["count"]
                                } for rating in food_review.json()["pageProps"]["cannedOutlet"]
                            ],
                        },

                        "range_prices": self.PRICE[str(food_review.json()["pageProps"]["outlet"]["priceLevel"])],
                        "restaurant_id": food_review.json()["pageProps"]["outlet"]["uid"],
                        "detail_reviews": ""
                    }


                    logger.info(f'city: {ingredient["city"]["name"].lower()}')
                    logger.info(f'restaurant: {ingredient["restaurant"]["path"].split("/")[-1]}')
                    logger.info(f'link: {header_required["link"]}')
                    logger.info(f'api review: {api_review}')
                    logger.info(f'restaurant name: {header_required["reviews_name"]}')
                    logger.info(f'card : {index}')
                    logger.info(f'total cards : {len(cards)}')
                    print()


                    header_required["tags"].append(self.DOMAIN)
                    self.__get_review(raw_json=header_required)

                except Exception as err:
                    ic({
                        "error": err,
                        "api_review": api_review,
                        "card": card
                    })
                    
                    self.__char.append(api_review)

    def __extract_city(self, city: str) -> None:
        response = self.__api.get(url=f'https://gofood.co.id/_next/data/{self.VERSION}/id{city["path"]}.json', max_retries=10)

        task_executor = []
        for index, restaurant in enumerate(response.json()["pageProps"]["contents"][0]["data"]): # Mengambil restaurant dari kota

            ic(index)
            ingredient = {
                "restaurant": restaurant,
                "city": city
            }

            self.__extract_restaurant(ingredient)
            # task_executor.append(self.__executor.submit(self.__extract_restaurant, ingredient))

        wait(task_executor)


    def main(self) -> None:

        cities = self.__gofood.collect_cities(self.API_CITY)
        # task_city_executor = []
        for city in cities: # Mengambil Kota
            self.__extract_city(city)

            # task_city_executor.append(self.__city_executor.submit(self.__extract_city, city))

        # wait(task_city_executor)


        ...