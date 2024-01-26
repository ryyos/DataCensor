

from typing import List
from pyquery import PyQuery

from utils import *

class AppsApkLibs:
    def __init__(self) -> None:
        ...

    def collect_apps(self, url_page: str) -> List[str]:
        response = self.__retry(url_page)
        html = PyQuery(response.text)

        apps = html.find('article.vce-post.post.type-post.status-publish.format-standard.has-post-thumbnail.hentry h2 a')

        return apps
            
    def write_detail(self, headers: dict, detail: dict):
        path_detail = f'{create_dir(headers=headers, website="appsapk")}/detail/{vname(headers["reviews_name"])}.json'

        headers.update({
            "path_data_raw": path_detail,
            "path_data_clean": self.__convert_path(path_detail)
        })

        headers["detail_application"].update({
            "descriptions": detail.find('#description').text()
        })

        File.write_json(path_detail, headers)

    def collect_reviews(self, url_app: str) -> List[dict]:
        all_reviews: List[dict] = []
        error: List[dict] = []

        comment_page = 1
        while True:

            url_review = f'{url_app}comment-page-{comment_page}/#comments'

            response = self.__retry(url_review)
            app = PyQuery(response.text)

            if response.status_code != 200:
                error.append({
                    "message": response.text,
                    "type": response.status_code,
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