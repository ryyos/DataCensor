import os
import requests
import json
import datetime as date

from time import time, strftime, sleep
from pyquery import PyQuery
from requests import Response
from typing import List
from icecream import ic
from requests_html import HTMLSession
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, wait
from zlib import crc32
from dotenv import *
from component import codes
from server.s3 import ConnectionS3
from library import SoftonicLibs
from ApiRetrys import ApiRetry
from dekimashita import Dekimashita

from utils import *


class Softonic:
    def __init__(self) -> None:
        load_dotenv()
        self.__logs = Logs(path_monitoring='logs/softonic/monitoring_data.json',
                            path_log='logs/softonic/monitoring_logs.json',
                            domain='en.softonic.com')
        
        self.__s3 = ConnectionS3(access_key_id=os.getenv('ACCESS_KEY_ID'),
                                 secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
                                 endpoint_url=os.getenv('ENDPOINT'),
                                 )

        self.__api = ApiRetry(show_logs=True, 
                              handle_forbidden=True, 
                              redirect_url='https://en.softonic.com/', 
                              defaulth_headers=True)
        
        self.__executor = ThreadPoolExecutor()
        self.__softonic = SoftonicLibs()
        self.__api = ApiRetry()
        
        self._bucket = os.getenv('BUCKET')
        
        self.logs: List[dict] = []

        self.MAIN_DOMAIN = 'en.softonic.com'
        self.MAIN_URL = 'https://en.softonic.com/'

        self.TYPES = [
            "new-apps",
            "trending",
            "date",
            "last-news",
            "new-versions"
        ]

        self.PLATFORMS = [
            "windows",
            "android",
            "mac",
            "iphone"
        ]

        self.RESPONSE_CODE = [200, 400, 404, 500]

        self.detail_reviews = []
        ...

    def __extract_review(self, raw_game: str) -> None: # halaman game
        url_game = raw_game["url_game"]

        ... # mengambil Header baku
        response = self.__api.get(url=url_game)
        headers = PyQuery(response.text)

        descriptions = headers.find('article.editor-review')

        descs = []
        for desc in descriptions.children():
            text = desc.text_content()

            if desc.tag == 'h2':

                content = {
                    "sub_title": text,
                    "sub_description": []
                }

                descs.append(content)
                
            elif desc.tag == 'p':
                descs[-1]["sub_description"].append(text)

        detail_game = {
            "id": crc32(Dekimashita.vdir(headers.find('head > title').text().split(' - ')[0]).encode('utf-8')),
            "title": headers.find('head > title').text().split(' - ')[0],
            "version": PyQuery(headers.find('li[data-meta="version"]')[-1]).text().replace('V ', '') if headers.find('li[data-meta="version"]') else None,
            "language": PyQuery(headers.find('ul[class="app-header__features"] > li[class="app-header__item"]')[1]).text(),
            "status": PyQuery(headers.find('ul[class="app-header__features"] > li[class="app-header__item"]')[0]).text(),
            "descriptions": descs,
            "related_topics": [PyQuery(relevant).text() for relevant in headers.find('ul.related-topics__list > li')],
        }

        for spec in headers.find('ul.app-specs__list > li'):
            detail_game.update(
                {
                    PyQuery(spec).find('h3').text(): PyQuery(spec).find('p').text()
                }
            )

        ... # menulis detail
        details: dict = self.__softonic.write_detail(headers=raw_game, detail_game=detail_game)
        # self.__s3.upload(key=details["path_detail"], 
        #                  body=details["data_detail"], 
        #                  bucket=self._bucket)

        ...

        reviews: dict = self.__softonic.get_reviews(url_game)

        logger.info(f'len reviews: {len(reviews["all_reviews"])}')

        total_error = 0
        for index, review in enumerate(reviews["all_reviews"]):
            
            ...

            detail_review = {
                "id_review": int(review["id"]),
                "username_reviews": review["author"]["name"],
                "image_reviews": review["author"]["avatar"]["permalink"],
                "created_time": review["createdAt"].replace('T', ' '),
                "created_time_epoch": convert_time(review["createdAt"]),
                "email_reviews": None,
                "company_name": None,
                "location_reviews": None,
                "title_detail_reviews": None,

                "total_reviews": len(reviews["all_reviews"]),
                "reviews_rating": {
                    "total_rating": PyQuery(reviews["html"].find('div.rating-info')[0]).text(),
                    "detail_total_rating": None
                },
                "detail_reviews_rating": [
                    {
                    "score_rating": None,
                    "category_rating": None
                    }
                ],
                "total_likes_reviews": review["likes"],
                "total_dislikes_reviews": review["dislikes"],
                "total_reply_reviews": 0,
                "content_reviews": PyQuery(review["raw_message"]).text(),
                "reply_content_reviews": [],
                "date_of_experience": review["createdAt"].replace('T', ' '),
                "date_of_experience_epoch": convert_time(review["createdAt"])
            }

            path = f'{self.__softonic.create_dir(raw_data=raw_game, main_path="data")}/{detail_review["id_review"]}.json'

            raw_game.update({
                "id": detail_game["id"],
                "detail_reviews": detail_review,
                "detail_applications": detail_game,
                "reviews_name": detail_game["title"],
                "path_data_raw": 'S3://ai-pipeline-statistics/'+path,
                "path_data_clean": 'S3://ai-pipeline-statistics/'+convert_path(path),
            })

            # response = self.__s3.upload(key=path, body=raw_game, bucket=self._bucket)
            File.write_json(path=path, content=raw_game)
            response = 200
            if index in [2,5,6,4,9,6,11,12]: response = 404

            error: int = self.__logs.logsS3(func=self.__logs,
                               header=raw_game,
                               index=index,
                               response=response,
                               all_reviews=reviews["all_reviews"],
                               error=reviews["error"],
                               total_err=total_error)

            total_error+=error
            reviews["error"].clear()

        if not reviews["all_reviews"]:
            self.__logs.zero(func=self.__logs,
                             header=raw_game)
            
        ic({
            "len all review": len(reviews["all_reviews"])
        })

        logger.info(f'application: {raw_game["url_game"]}')
        logger.info(f'category: {raw_game["categories"]}')
        logger.info(f'type: {raw_game["type"]}')
        logger.info(f'total review: {len(reviews["all_reviews"])}')

        ...

    def __extract_game(self, url_game: str) -> None:
        ic(url_game)
        response = self.__api.get(url=url_game["url"].replace('/comments', ''))

        results_header = {
            "link": self.MAIN_URL,
            "domain": self.MAIN_DOMAIN,
            "tags": [self.MAIN_DOMAIN],
            "crawling_time": strftime('%Y-%m-%d %H:%M:%S'),
            "crawling_time_epoch": int(time()),
            "path_data_raw": "",
            "path_data_clean": "",
            "reviews_name": "name_game",
            "location_reviews": None,
            "category_reviews": "application",
            "url_game": url_game["url"],
            "type": PyQuery(response.text).find('meta[property="rv-recat"]').attr('content').split(',')[0],
            "categories": PyQuery(response.text).find('meta[property="rv-recat"]').attr('content').split(',')[-1],
            "platform": url_game["platform"]
        }

        self.__extract_review(raw_game=results_header)

        ...

    def main(self):

        for platform in self.PLATFORMS:
            categories_urls = self.__softonic.collect_categories(url=self.MAIN_URL+platform)

            for categories in categories_urls:

                for type in self.TYPES:
                    games = self.__softonic.collect_games(url=f'{categories}:{type}')

                    task_executor = []
                    for index, game in enumerate(games):

                        ic(f'game: {game}')
                        ic(f'game to: {index}')

                        igredation = {
                            "platform": platform,
                            "url": game
                        }

                        ic(igredation)
                        
                        # self.__extract_game(igredation)
                        task_executor.append(self.__executor.submit(self.__extract_game, igredation))
                        ...
                    wait(task_executor)
                    ...
                ...
            ...
        ...
        self.__executor.shutdown(wait=True)