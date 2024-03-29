import os

from typing import List
from pyquery import PyQuery
from dotenv import load_dotenv

from server.s3 import ConnectionS3
from components import codes
from ApiRetrys import ApiRetry
from dekimashita import Dekimashita
from components import AppsApkComponent
from utils import *

class AppsApkLibs(AppsApkComponent):
    def __init__(self, save: bool) -> None:
        super().__init__()
        load_dotenv()

        self.api = ApiRetry(defaulth_headers=True, show_logs=True, handle_forbidden=True, redirect_url='https://www.appsapk.com')
        self.logs = Logs(path_monitoring='logs/appsapk/monitoring_data.json',
                            path_log='logs/appsapk/monitoring_logs.json',
                            domain='www.appsapk.com')
        
        self.s3 = ConnectionS3(access_key_id=os.getenv('ACCESS_KEY_ID'),
                                 secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
                                 endpoint_url=os.getenv('ENDPOINT'),
                                 )
        

        self.SAVE_TO_LOKAL = save

        ...

    def collect_apps(self, url_page: str) -> List[str]:
        response = self.api.get(url=url_page)
        html = PyQuery(response.text)

        apps = html.find('article.vce-post.post.type-post.status-publish.format-standard.has-post-thumbnail.hentry h2 a')

        return apps
        ...
            
    def write_detail(self, headers: dict):
        path_detail = f'{create_dir(headers=headers, website="appsapk")}/detail/{Dekimashita.vtext(headers["reviews_name"]).replace(" ", "_")}.json'

        headers.update({
            "path_data_raw": path_detail,
            "path_data_clean": convert_path(path_detail)
        })

        if self.SAVE_TO_LOKAL:
            File.write_json(path_detail, headers)
        
        ...

    def collect_reviews(self, url_app: str) -> List[dict]:
        all_reviews: List[dict] = []
        error: List[dict] = []

        comment_page = 1
        while True:

            url_review = f'{url_app}comment-page-{comment_page}/#comments'

            response = self.api.get(url=url_review)
            app = PyQuery(response.text)

            if response.status_code != 200:
                error.append({
                    "message": response.text,
                    "type": codes[str(response.status_code)],
                    "id": None
                })

                break
            comment_page +=1

            if not app.find('ul[class="comment-list"] > li'): break

            for review in app.find('ul[class="comment-list"] > li'):
                all_reviews.append(review)

            
        return {
            "all_reviews": all_reviews,
            "error": error
        }
            

        ...