import os
import requests

from time import time, strftime, sleep
from pyquery import PyQuery
from concurrent.futures import ThreadPoolExecutor, wait
from zlib import crc32
from library import SoftonicLibs
from dekimashita import Dekimashita

from utils import *


class Softonic(SoftonicLibs):
    def __init__(self, s3: bool, save: bool, thread: bool) -> None:
        super().__init__(save)
        
        self.__executor = ThreadPoolExecutor()

        self.SAVE_TO_S3 = s3
        self.SAVE_TO_LOKAL = save
        self.USING_THREADS = thread

        ...

    def __extract_review(self, raw_game: str) -> None: # halaman game
        url_game = raw_game["url_game"]

        ... # mengambil Header baku
        response = self.api.get(url=url_game)
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
        (path_detail, data_detail) = self.write_detail(headers=raw_game, detail_game=detail_game)

        if self.SAVE_TO_LOKAL:
            File.write_json(path_detail, data_detail)

        if self.SAVE_TO_S3: 
            self.s3.upload(key=path_detail, 
                         body=data_detail, 
                         bucket=self.bucket)

        ...

        reviews: dict = self.get_reviews(url_game)

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

            path = f'{self.create_dir(raw_data=raw_game, main_path="data")}/{detail_review["id_review"]}.json'

            raw_game.update({
                "id": detail_game["id"],
                "detail_reviews": detail_review,
                "detail_applications": detail_game,
                "reviews_name": detail_game["title"],
                "path_data_raw": 'S3://ai-pipeline-statistics/'+path,
                "path_data_clean": 'S3://ai-pipeline-statistics/'+convert_path(path),
            })

            if self.SAVE_TO_S3: 
                response = self.s3.upload(key=path, body=raw_game, bucket=self.bucket)
            else: 
                response = 200
            
            if self.SAVE_TO_LOKAL:
                File.write_json(path=path, content=raw_game)

            error: int = self.logs.logsS3(func=self.logs,
                               header=raw_game,
                               index=index,
                               response=response,
                               all_reviews=reviews["all_reviews"],
                               error=reviews["error"],
                               total_err=total_error)

            total_error+=error
            reviews["error"].clear()

        if not reviews["all_reviews"]:
            self.logs.zero(func=self.logs,
                             header=raw_game)
        ...

    def __extract_game(self, url_game: str) -> None:
        response = self.api.get(url=url_game["url"].replace('/comments', ''))

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
            categories_urls = self.collect_categories(url=self.MAIN_URL+platform)

            for categories in categories_urls:

                for type in self.TYPES:
                    games = self.collect_games(url=f'{categories}:{type}')

                    task_executor = []
                    for index, game in enumerate(games):

                        igredation = {
                            "platform": platform,
                            "url": game
                        }
                        
                        if self.USING_THREADS: 
                            task_executor.append(self.__executor.submit(self.__extract_game, igredation))
                        else: 
                            self.__extract_game(igredation)

                        ...
                    wait(task_executor)
                    ...
                ...
            ...
        ...
        self.__executor.shutdown(wait=True)