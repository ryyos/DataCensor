import os
import requests
import datetime as date

from random import randint
from zlib import crc32
from datetime import datetime, timezone
from time import strftime, sleep, time
from icecream import ic
from pyquery import PyQuery
from dekimashita import Dekimashita
from requests import Session, Response
from fake_useragent import FakeUserAgent
from concurrent.futures import ThreadPoolExecutor, wait
from typing import List
from components import codes

from library import AppsApkLibs
from ApiRetrys import ApiRetry

from utils import *
from dotenv import *

class AppsApk(AppsApkLibs):
    def __init__(self) -> None:
        super().__init__()

        self.__executor = ThreadPoolExecutor(max_workers=5)
        self.__appsapk = AppsApkLibs()

        self.MAIN_DOMAIN = 'www.appsapk.com'
        self.MAIN_URL = 'https://www.appsapk.com'
        self.MAIN_PATH = 'data'
        
        ...

    def __extract_app(self, url_app: PyQuery) -> dict:
        response = self.api.get(url=url_app)
        app = PyQuery(response.text)

        try: int(total_review = app.find('h3[class="comment-title main-box-title"]').text().split(' ')[0])
        except Exception: total_review = None

        logger.info(f'total review: {total_review}')
        logger.info(f'url_app: {url_app}')

        results = {
            "link": self.MAIN_URL,
            "domain": self.MAIN_DOMAIN,
            "id": crc32(Dekimashita.vdir(app.find('h1[class="entry-title"]').text()).encode('utf-8')),
            "tags": [PyQuery(tag).text() for tag in app.find('a[rel="tag"]')],
            "crawling_time": strftime('%Y-%m-%d %H:%M:%S'),
            "crawling_time_epoch": int(time()),
            "path_data_raw": "string",
            "path_data_clean": "string",
            "reviews_name": app.find('h1[class="entry-title"]').text(),
            "location_reviews": None,
            "category_reviews": "application",
        
            "total_reviews": total_review,
            "reviews_rating": {
            "total_rating": None,
            "detail_total_rating": [
                {
                "score_rating": None,
                "category_rating": None
                }
            ]
            },
            "detail_application": {
                Dekimashita.vdir(PyQuery(detail).find('strong').text()): Dekimashita.vtext(PyQuery(detail).text().replace(PyQuery(detail).find('strong').text(), '').replace('\n', ''))\
                for detail in app.find('div[class="details"]')
            }
        }
        
        results["detail_application"].update({
            "descriptions": app.find('#description').text()
        })

        path_detail = f'{create_dir(headers=results, website="appsapk")}/detail/{Dekimashita.vdir(results["reviews_name"])}.json'

        results["tags"].append(self.MAIN_DOMAIN)
        results.update({
            "path_data_raw": 'S3://ai-pipeline-statistics/'+path_detail,
            "path_data_clean": 'S3://ai-pipeline-statistics/'+convert_path(path_detail)
        })

        try:
            response = self.s3.upload(key=path_detail, body=results, bucket=self.bucket)
            ic(response)
            # self.__appsapk.write_detail(headers=results)
        except Exception as err:
            ic(err)

        return results
        ...

    def __extract_reviews(self, url_app: str) -> None:

        header: dict = self.__extract_app(url_app)

        reviews: dict = self.__appsapk.collect_reviews(url_app)

        total_error = 0
        for index, review in enumerate(reviews["all_reviews"]):
            
            header.update({
                "detail_reviews": {
                "id_review": crc32(Dekimashita.vdir(PyQuery(list(PyQuery(review).find('div[class="comment-author vcard"] > b'))[0]).text()).encode('utf-8')),
                "username_reviews": PyQuery(list(PyQuery(review).find('div[class="comment-author vcard"] > b'))[0]).text(),
                "image_reviews": PyQuery(review).find('div[class="app-icon"]').attr('src'),
                "created_time": PyQuery(list(PyQuery(review).find('div[class="comment-metadata"] time'))[0]).attr('datetime').split('+')[0].replace('T', ' '),
                "created_time_epoch": convert_time(PyQuery(list(PyQuery(review).find('div[class="comment-metadata"] time'))[0]).attr('datetime')),
                "email_reviews": None,
                "company_name": None,
                "location_reviews": None,
                "title_detail_reviews": None,
                "reviews_rating": None,
                "detail_reviews_rating": [
                    {
                    "score_rating": None,
                    "category_rating": None
                    }
                ],
                "total_likes_reviews": None,
                "total_dislikes_reviews": None,
                "total_reply_reviews": 0,
                "content_reviews": Dekimashita.vtext(PyQuery(list(PyQuery(review).find('div[class="comment-content"]'))[0]).text()),
                "reply_content_reviews": [],
                "date_of_experience": PyQuery(list(PyQuery(review).find('div[class="comment-metadata"] time'))[0]).attr('datetime').split('+')[0].replace('T', ' '),
                "date_of_experience_epoch": convert_time(PyQuery(list(PyQuery(review).find('div[class="comment-metadata"] time'))[0]).attr('datetime'))
                }
            })

            logger.info(f'username: {header["detail_reviews"]["username_reviews"]}')

            ic(bool(PyQuery(review).find('ul[class="children"]')))
            if PyQuery(review).find('ul[class="children"]'):
                child = PyQuery(review).find('ul[class="children"]')
                for reply in PyQuery(child).find('li'):
                    header["detail_reviews"]["total_reply_reviews"] +=1
                    header["detail_reviews"]["reply_content_reviews"].append({
                        "username_reply_reviews": PyQuery(reply).find('div[class="comment-author vcard"] > b').text(),
                        "content_reviews": Dekimashita.vtext(PyQuery(reply).find('div[class="comment-content"]').text())
                    })

            path = f'{create_dir(headers=header, website="appsapk")}/{Dekimashita.vdir(header["detail_reviews"]["username_reviews"])}.json'

            header.update({
                "path_data_raw": 'S3://ai-pipeline-statistics/'+path,
                "path_data_clean": 'S3://ai-pipeline-statistics/'+convert_path(path)
            })

            response = self.s3.upload(key=path, body=header, bucket=self.bucket)

            # response = 200
            # if index in [2,5,6,4,9,6,11,12]: response = 404

            error: int = self.logs.logsS3(func=self.logs,
                               header=header,
                               index=index,
                               response=response,
                               all_reviews=reviews["all_reviews"],
                               error=reviews["error"],
                               total_err=total_error)


            total_error+=error
            reviews["error"].clear()

        if not reviews["all_reviews"]:
            self.logs.zero(func=self.logs,
                             header=header)
        ...

    def main(self):

        page = 1
        while True:
            url = f'{self.MAIN_URL}/page/{page}'
            page +=1
            apps = self.__appsapk.collect_apps(url)

            task_executor = []
            for app in apps:
                # task_executor.append(self.__executor.submit(self.__extract_reviews, PyQuery(app).attr('href')))

                self.__extract_reviews(PyQuery(app).attr('href'))
            # wait(task_executor)
            if not apps: break
        # self.__executor.shutdown(wait=True)
        ...