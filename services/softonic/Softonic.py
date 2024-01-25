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

from library import SoftonicLibs

from utils import *

class Softonic:
    def __init__(self) -> None:

        self.__logging = Logs()
        self.__executor = ThreadPoolExecutor(max_workers=10)
        self.__softonic = SoftonicLibs()

        self.__datas: List[dict] = []
        self.__monitorings: List[dict] = []
        self.logs: List[dict] = []

        self.PIC = 'Rio Dwi Saputra'
        self.MAIN_PATH = 'data'
        self.platform = ''

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
        response = self.__retry(url=url_game)
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

        ... 

        ... # Write only detail


        raw_game["reviews_name"] = detail_game["title"]
        ic(raw_game["reviews_name"])

        path_detail = f'{self.__create_dir(raw_game)}/detail/{vname(detail_game["title"])}.json'

        raw_game.update({
            "detail_applications": detail_game,
            "path_data_raw": path_detail,
            "path_data_clean": self.__convert_path(path_detail)
        })

        self.__file.write_json(path_detail, raw_game)
        ...

        ... # request to comments param

        response = self.__retry(url=f'{url_game}/comments')
        html = PyQuery(response.text)

        game_title = html.find('head > title:first-child')
        ...

        ... # extract disqus review

        response = self.__retry(url=self.__build_param_disqus(name_apk=game_title, url_apk=url_game))

        disqus_page = PyQuery(response.text)
        reviews_temp = json.loads(disqus_page.find('#disqus-threadData').text())

        all_reviews = []
        total_error = 0

        ic(len(reviews_temp["response"]["posts"]))

        for review in reviews_temp["response"]["posts"]:
            
            all_reviews.append(review)

        try:
            cursor = reviews_temp["cursor"]["next"]
            thread = reviews_temp["response"]["posts"][0]["thread"]

            while True:

                reviews = self.__retry(url=self.__param_second_cursor(
                    thread=thread,
                    cursor=cursor)).json()

                if not reviews["cursor"]["hasNext"]: break
                
                if response.status_code != 200:
                    total_error+=1
                    break

                cursor = reviews["cursor"]["next"]
                logger.info(f'cursor: {cursor}')


                for review in reviews["response"]:
                    all_reviews.append(review)

        except Exception as err:
            ...

        ic(len(all_reviews))

        temporarys = []
        for index, review in enumerate(all_reviews):
            
            ... # Logging
            self.__logging(id_product=crc32(vname(detail_game["title"]).encode('utf-8')),
                           id_review=review["id"],
                           status_conditions='on progress',
                           status_runtime='success',
                           total=len(all_reviews),
                           success=index,
                           failed=0,
                           sub_source=detail_game["title"],
                           message=None,
                           type_error=None)

            ...

            if review["parent"]:
                for parent in temporarys:
                    if parent["id"] == review["parent"]:
                        parent["reply_content_reviews"].append({
                            "username_reply_reviews":  review["author"]["name"],
                            "content_reviews": review["raw_message"]
                        })
                        parent["total_reply_reviews"] +=1
            
            else:
                detail_review = {
                    "id": int(review["id"]),
                    "username_reviews": review["author"]["name"],
                    "image_reviews": 'https:'+review["author"]["avatar"]["permalink"],
                    "created_time": review["createdAt"].replace('T', ' '),
                    "created_time_epoch": self.__convert_time(review["createdAt"]),
                    "email_reviews": None,
                    "company_name": None,
                    "location_reviews": None,
                    "title_detail_reviews": None,

                    "total_reviews": len(all_reviews),
                    "reviews_rating": {
                        "total_rating": PyQuery(html.find('div.rating-info')[0]).text(),
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
                    "date_of_experience_epoch": self.__convert_time(review["createdAt"])
                }

                path = f'{self.__create_dir(raw_data=raw_game)}/{detail_review["id"]}.json'


                raw_game.update({
                    "detail_reviews": detail_review,
                    "detail_applications": detail_game,
                    "reviews_name": detail_game["title"],
                    "path_data_raw": path,
                    "path_data_clean": self.__convert_path(path),
                })

                self.__file.write_json(path=path, content=raw_game)


        if total_error:    
            message="failed request to api review"
            type_error="request failed"
            runtime = 'error'
        else:
            message = None
            runtime = 'success'
            type_error = None

        self.__logging(id_product=crc32(vname(detail_game["title"]).encode('utf-8')),
                        id_review=review["id"],
                        status_conditions=runtime,
                        status_runtime='error',
                        total=len(all_reviews),
                        success=len(all_reviews),
                        failed=total_error,
                        sub_source=detail_game["title"],
                        message=message,
                        type_error=type_error)
    

        for detail in temporarys:

            raw_game.update({
                "detail_reviews": detail,
                "detail_applications": detail_game,
                "reviews_name": detail_game["title"],
            })

            path = f'{self.__create_dir(raw_data=raw_game)}/{detail["id"]}.json'

            raw_game.update({
                "path_data_raw": path,
                "path_data_clean": self.__convert_path(path),
            })

            self.__file.write_json(path=path, content=raw_game)

        ic({
            "len all review": len(all_reviews),
            "len temp": len(temporarys),
            "find review": len(reviews_temp["response"]["posts"])
        })

        logger.info(f'application: {raw_game["url_game"]}')
        logger.info(f'category: {raw_game["categories"]}')
        logger.info(f'type: {raw_game["type"]}')
        logger.info(f'total review: {len(all_reviews)}')

        ...

    def __extract_game(self, url_game: str) -> None:
        ic(url_game)
        response = self.__retry(url=url_game["url"].replace('/comments', ''))

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
                        
                        # self.__extract_game(game)
                        task_executor.append(self.__executor.submit(self.__extract_game, igredation))
                        ...
                    wait(task_executor)
                    ...
                ...
            ...
        ...
        self.__executor.shutdown(wait=True)