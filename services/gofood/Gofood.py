import os
import datetime as date
import requests
import json

from zlib import crc32
from time import time
from icecream import ic
from typing import List
from dekimashita import Dekimashita
from dotenv import *

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait

from library import GofoodLibs
from utils import *

class Gofood(GofoodLibs):
    def __init__(self, s3: bool, save: bool, thread: bool) -> None:
        super().__init__(save)

        self.__executor = ThreadPoolExecutor()

        self.SAVE_TO_S3 = s3
        self.SAVE_TO_LOKAL = save
        self.USING_THREADS = thread


    def __get_review(self, raw_json: dict):
        details: dict = self.write_detail(raw_json)

        if self.SAVE_TO_S3: 
            self.s3.upload(key=details["path_detail"], body=details["data_detail"], bucket=self.bucket)

        if self.SAVE_TO_LOKAL:
            File.write_json(path=details["path_detail"], content=details["data_detail"])

        reviews: dict = self.collect_reviews(raw_json)
        raw_json["total_reviews"] = len(reviews["all_reviews"])
        
        total_error = 0
        for index, comment in enumerate(reviews["all_reviews"]):
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

            path_data = self.create_dir(raw_data=raw_json, create=self.SAVE_TO_LOKAL)
            detail_reviews["tags_review"].append(self.DOMAIN)

            raw_json.update({
                "detail_reviews": detail_reviews,
                "path_data_raw": f'S3://ai-pipeline-statistics/{path_data}/{detail_reviews["id_review"]}.json',
                "path_data_clean": f'S3://ai-pipeline-statistics/{convert_path(path_data)}/{detail_reviews["id_review"]}.json'
            })

            if self.SAVE_TO_S3: 
                response = self.s3.upload(key=f'{path_data}/{detail_reviews["id_review"]}.json', body=raw_json, bucket=self.bucket)
            else: 
                response = 200

            if self.SAVE_TO_LOKAL: 
                File.write_json(path=f'{path_data}/{detail_reviews["id_review"]}.json', content=raw_json)

            error: int = self.logs.logsS3(func=self.logs,
                               header=raw_json,
                               index=index,
                               response=response,
                               all_reviews=reviews["all_reviews"],
                               error=reviews["error"],
                               total_err=total_error)

            total_error+=error
            reviews["error"].clear()

        if not reviews["all_reviews"]:
            self.logs.zero(func=self.logs,
                             header=raw_json)
        ...

    def __extract_restaurant(self, ingredient: dict):
            cards: List[str] = self.collect_card_restaurant(restaurant=ingredient["restaurant"]["path"]) # Mengambil card restaurant dari area

            for card in cards:

                """ api_review

                Param:
                    card | /ketapang/restaurant/pempek-bang-awie-wenang-a906c98d-2d31-48bc-8408-82dc1350cdca
                
                """
                api_review = f'https://gofood.co.id/_next/data/{self.VERSION}/id{card}/reviews.json?id={card.split("/")[-1]}'
                
            
                try:
                    food_review = self.api.get(url=api_review, max_retries=30)

                    # Jika di redirect maka ambil destination dan request ke path yang di berikan
                    if food_review.json()["pageProps"].get("__N_REDIRECT", None):
                        food_review = self.api.get(url=f'https://gofood.co.id/_next/data/{self.VERSION}/id{food_review.json()["pageProps"]["__N_REDIRECT"]}/reviews.json?id={card.split("/")[-1]}', max_retries=30)


                    header_required = {
                        "id": crc32(Dekimashita.vdir(food_review.json()["pageProps"]["outlet"]["core"]["displayName"]).encode('utf-8')),
                        "link": self.MAIN_URL+food_review.json()["pageProps"].get("outletUrl"),
                        "domain": self.DOMAIN,
                        "tags": [tag["displayName"] for tag in food_review.json()["pageProps"]["outlet"]["core"]["tags"]],
                        "crawling_time": now(),
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


                    header_required["tags"].append(self.DOMAIN)
                    self.__get_review(raw_json=header_required)

                except Exception as err:
                    ic({
                        "error": err,
                        "api_review": api_review,
                        "card": card
                    })
                    

    def __extract_city(self, city: str) -> None:
        response = self.api.get(url=f'https://gofood.co.id/_next/data/{self.VERSION}/id{city["path"]}.json', max_retries=10)

        task_executor = []
        for restaurant in response.json()["pageProps"]["contents"][0]["data"]: # Mengambil restaurant dari kota

            ingredient = {
                "restaurant": restaurant,
                "city": city
            }

            if self.USING_THREADS: task_executor.append(self.__executor.submit(self.__extract_restaurant, ingredient))
            else: self.__extract_restaurant(ingredient)

        wait(task_executor)


    def main(self) -> None:

        cities = self.collect_cities(self.API_CITY)
        for city in cities: # Mengambil Kota
            self.__extract_city(city)

        
        self.__executor.shutdown(wait=True)

        ...