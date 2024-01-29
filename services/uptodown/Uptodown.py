import os

from library import UptodownLibs
from requests import Response
from time import time, sleep
from pyquery import PyQuery
from typing import List
from icecream import ic
from dotenv import load_dotenv
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, wait
from server.s3 import ConnectionS3
from utils import *

class Uptodown:
    def __init__(self) -> None:
        load_dotenv()
        self.__platforms = ['android', 'windows', 'mac']

        self.__MAIN_URL = 'https://id.uptodown.com/'
        self.__DOMAIN = 'id.uptodown.com'

        self.parser = Parser()
        self.__uptodown = UptodownLibs()
        self.__executor = ThreadPoolExecutor()

        self.__logs = Logs(path_monitoring='logs/uptodown/monitoring_data.json',
                            path_log='logs/uptodown/monitoring_logs.json',
                            domain='id.uptodown.com')

        self.__bucket = os.getenv('BUCKET')
        self.__s3 = ConnectionS3(access_key_id=os.getenv('ACCESS_KEY_ID'),
                                 secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
                                 endpoint_url=os.getenv('ENDPOINT'),
                                 )
        ...

    def extract_review(self, header: dict) -> None:
        url_app = self.__uptodown.selection_url(header["link"])
        response = self.__uptodown.api.get(f'{url_app}/mng/v2/app/{header["id"]}/comments', headers=self.__uptodown.headers)

        reviews = PyQuery(response.json()['content'])

        all_reviews: List[dict] = []

        for review in reviews.find('div.comment'):
            temp = {
                "id_review": int(PyQuery(review).attr('id')),
                "username_reviews": self.__uptodown.strip(self.parser.ex(review, 'span.user').text()),
                "image_reviews": PyQuery(self.parser.ex(review, 'img')[0]).attr('src'),
                "created_time": self.__uptodown.strip(self.parser.ex(review, 'span:nth-child(3)').text()),
                "created_time_epoch": None,
                "email_reviews": None,
                "company_name": None,
                "location_reviews": None,
                "title_detail_reviews": None,
                "reviews_rating": len(self.parser.ex(review, 'img.active')),
                "detail_reviews_rating": [
                    {
                      "score_rating": None,
                      "category_rating": None,
                    }
                ],
                "content_reviews": self.parser.ex(review, 'p').text(),
                "total_likes_reviews": self.__uptodown.handler(self.parser, review, 'div[name="favs-icon"] span', 'Like'),
                "total_dislikes_reviews": None,
                "total_reply_reviews":  self.__uptodown.handler(self.parser, review, 'div[name="response-icon"] span', 'Balas'),
                "reply_content_reviews": [],
                "date_of_experience": None,
                "date_of_experience_epoch": None
            }

            if temp["total_reply_reviews"]: temp["reply_content_reviews"] = self.__uptodown.get_reply(url_app=header["link"], id=temp["id_review"])
            all_reviews.append(temp)
        
        reviews = self.__uptodown.get_next_review(url_app, header["id"])

        for review in reviews["all_reviews"]:
            temp = {
                "id_review": review["id"],
                "username_reviews": review["userName"],
                "image_reviews": review["icon"],
                "created_time": review["timeAgo"],
                "created_time_epoch": None,
                "email_reviews": None,
                "company_name": None,
                "location_reviews": None,
                "title_detail_reviews": None,
                "reviews_rating": review["rating"],
                "detail_reviews_rating": [
                    {
                      "score_rating": None,
                      "category_rating": None,
                    }
                ],
                "total_likes_reviews": review["likes"],
                "total_dislikes_reviews": None,
                "content_reviews": review["text"],
                "total_reply_reviews": review["totalAnswers"],
                "reply_content_reviews": [],
                "date_of_experience": None,
                "date_of_experience_epoch": None
            }

            if temp["total_reply_reviews"]: temp["reply_content_reviews"] = self.__uptodown.get_reply(url_app=header["link"], id=temp["id_review"])
            all_reviews.append(temp)

        total_error = 0
        ic(len(all_reviews))
        for index, review in tqdm(enumerate(all_reviews), smoothing=0.1, total=len(all_reviews)):

            path = f'{self.__uptodown.create_dir(header, header)}/{vname(review["username_reviews"].lower())}.json'

            header.update({
                "detail_reviews": review,
                "path_data_raw": 'S3://ai-pipeline-statistics/'+path,
                "path_data_clean": 'S3://ai-pipeline-statistics/'+convert_path(path)
            })

            # response = self.__s3.upload(key=path,
            #                             body=header,
            #                             bucket=self.__bucket)

            response = 200
            # if index in [2,5,6,4,9,6,11,12]: response = 404

            File.write_json(path, header)
            
        #     error: int = self.__logs.logsS3(func=self.__logs,
        #                        header=header,
        #                        index=index,
        #                        response=response,
        #                        reviews=reviews,
        #                        total_err=total_error)

        #     total_error+=error
        #     reviews["error"].clear()

        # if not all_reviews:
        #     self.__logs.zero(func=self.__logs,
        #                      header=header)
        
        ...

    
    def extract_detail(self, component: dict) -> None:
        response: Response = self.__uptodown.api.get(url=component["app"], headers=self.__uptodown.headers)
        html = PyQuery(response.text)

        header = {
            "id": html.find('#detail-app-name').attr('code'),
            "link": component["app"],
            "domain": self.__DOMAIN,
            "crawling_time": now(),
            "crawling_time_epoch": int(time()),
            "path_data_raw": "",
            "path_data_clean": "",
            "reviews_name": html.find('#detail-app-name').text(),
            "location_reviews": None,
            "category_reviews": "application",
            "total_reviews": self.__uptodown.filter_total_review(html.find('#more-comments-rate-section').text()),
            "reviews_rating": {
              "total_rating": self.__uptodown.filter_rating(html.find('#rating').text()),
              "detail_total_rating": [
                {
                  "score_rating": None,
                  "category_rating": None
                }
              ]
            },
            "type": component["type"],
            "platform": component["platform"],
            "detail_application": ""
        }

        header["detail_application"] = {
            "title": html.find('#detail-app-name').text(),
            "information": html.find('div.detail > h2').text(),
            "version": html.find('div.version').text(),
            "author": html.find('div.autor a').text(),
            "descriptions": html.find('div.text-description p').text(),
            "technical-information": {
                PyQuery(key).find('td:nth-child(2)').text(): PyQuery(key).find('td:last-child').text() for key in html.find('#technical-information tr')
            },
            "previous_version": [
                {
                    "version": PyQuery(prev).find('span.version').text(),
                    "date": PyQuery(prev).find('span.date').text(),
                    "sdk": PyQuery(prev).find('span.sdkVersion').text()
                } for prev in html.find('#versions-items-list > div')
            ]
        }

        path_detail = f'{self.__uptodown.create_dir(header, component)}/detail/{vname(header["reviews_name"].lower())}.json'

        header.update({
            "path_data_raw": 'S3://ai-pipeline-statistics/'+path_detail,
            "path_data_clean": 'S3://ai-pipeline-statistics/+'+convert_path(path_detail)
        })

        # self.__s3.upload(key=path_detail,
        #                  body=header,
        #                  bucket=self.__bucket)

        File.write_json(path=path_detail, content=header)

        self.extract_review(header)
        ...


    def main(self) -> None:
        for platform in self.__platforms:
            types: List[str] = self.__uptodown.collect_types(self.__MAIN_URL+platform)

            for type in types:
                apps: List[str] = self.__uptodown.collect_apps(type)
                
                task_executor = []
                for app in apps:

                    component = {
                        "platform": platform,
                        "type": type.split('/')[-1],
                        "app": app
                    }

                    # self.extract_detail(component)
                    task_executor.append(self.__executor.submit(self.extract_detail, component))
                wait(task_executor)
        
        self.__executor.shutdown(wait=True)
                    



        ...
    