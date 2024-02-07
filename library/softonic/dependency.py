import json
import os

from zlib import crc32
from typing import Tuple, List
from requests import Response
from pyquery import PyQuery
from ApiRetrys import ApiRetry
from dekimashita import Dekimashita
from server.s3 import ConnectionS3
from utils import *

class SoftonicLibs:
    def __init__(self) -> None:

        self.api = ApiRetry(show_logs=False, 
                              handle_forbidden=True, 
                              redirect_url='https://en.softonic.com/', 
                              defaulth_headers=True)
        
        self.logs = Logs(path_monitoring='logs/softonic/monitoring_data.json',
                            path_log='logs/softonic/monitoring_logs.json',
                            domain='en.softonic.com')
        
        self.s3 = ConnectionS3(access_key_id=os.getenv('ACCESS_KEY_ID'),
                                 secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
                                 endpoint_url=os.getenv('ENDPOINT'),
                                 )
        
        self._bucket = os.getenv('BUCKET')

        self.API_REVIEW = 'https://disqus.com/api/3.0/threads/listPostsThreaded'
        self.API_KEY = 'E8Uh5l5fHZ6gD8U3KycjAIAk46f68Zw7C6eW8WSjZvCLXebZ7p0r1yrYDrLilk2F'
        self.DISQUS_API_COMMENT = 'https://disqus.com/embed/comments'
        self.MAIN_DOMAIN = 'en.softonic.com'
        self.MAIN_URL = 'https://en.softonic.com/'
        ...
        
    def collect_categories(self, url: str) -> List[str]:
        response: Response = self.api.get(url=url)
        html = PyQuery(response.text)

        categories_urls = [PyQuery(categories).attr('href') for categories in html.find('#sidenav-menu a[class="menu-categories__link"]')]
        
        return categories_urls
        ...

    def collect_games(self, url: str):
        response = self.api.get(url=url)
        
        games = []
        page = 1
        while True:
            html = PyQuery(response.text)

            for game in html.find('a[data-meta="app"]'): games.append(PyQuery(game).attr('href'))

            response: Response = self.api.get(url=f'{url}/{page}')

            if page > 1 and response.history: break

            page+=1

            if response.status_code != 200: break
            if not html.find('a[data-meta="app"]'): break

        return games
        ...
    

    def param_second_cursor(self, cursor: str, thread: str) -> str:

        return f'https://disqus.com/api/3.0/threads/listPostsThreaded?limit=20&thread={thread}&forum=en-softonic-com&order=popular&cursor={cursor}&api_key={self.API_KEY}'
        ...


    def build_param_disqus(self, url_apk: str, name_apk: str) -> str:
        return f'{self.DISQUS_API_COMMENT}/?base=default&f=en-softonic-com&t_u={url_apk}/comments&t_d={name_apk}&s_o=default#version=cb3f36bfade5c758ef967a494d077f95'
        ...
    def create_dir(self, raw_data: dict, main_path: str) -> str:
        try: os.makedirs(f'{main_path}/data_raw/data_review/softonic/{raw_data["platform"]}/{raw_data["type"]}/{raw_data["categories"]}/{Dekimashita.vdir(raw_data["reviews_name"].lower())}/json/detail')
        except Exception: ...
        finally: return f'{main_path}/data_raw/data_review/softonic/{raw_data["platform"]}/{raw_data["type"]}/{raw_data["categories"]}/{Dekimashita.vdir(raw_data["reviews_name"].lower())}/json'
        ...

    def get_reviews(self, url_game: str):

        response = self.api.get(url=f'{url_game}/comments')
        html = PyQuery(response.text)

        game_title = html.find('head > title:first-child')
        ...

        ... # extract disqus review

        response = self.api.get(url=self.build_param_disqus(name_apk=game_title, url_apk=url_game))

        disqus_page = PyQuery(response.text)
        reviews_temp = json.loads(disqus_page.find('#disqus-threadData').text())

        all_reviews: List[dict] = []
        error: List[dict] = []

        for review in reviews_temp["response"]["posts"]:
            if review["parent"]:
                for parent in all_reviews:
                    if parent["id"] == review["parent"]:
                        parent["reply_content_reviews"].append({
                            "username_reply_reviews":  review["author"]["name"],
                            "content_reviews": review["raw_message"]
                        })
                        parent["total_reply_reviews"] +=1

            else:
                all_reviews.append(review)

        try:
            cursor = reviews_temp["cursor"]["next"]
            thread = reviews_temp["response"]["posts"][0]["thread"]

            while True:

                reviews = self.api.get(url=self.param_second_cursor(thread=thread,cursor=cursor)).json()

                if not reviews["cursor"]["hasNext"]: break
                
                if response.status_code != 200:
                    error.append({
                        "message": response.text,
                        "type": response.status_code,
                        "id": None
                    })
                    break

                cursor = reviews["cursor"]["next"]
                logger.info(f'cursor: {cursor}')


                for review in reviews["response"]:
                    if review["parent"]:
                        for parent in all_reviews:
                            if parent["id"] == review["parent"]:
                                parent["reply_content_reviews"].append({
                                    "username_reply_reviews":  review["author"]["name"],
                                    "content_reviews": review["raw_message"]
                                })
                                parent["total_reply_reviews"] +=1

                    else:
                        all_reviews.append(review)

        except Exception as err:
            ...

        return {
            "all_reviews": all_reviews,
            "html": html,
            "error": error
        }

    def write_detail(self, headers: dict, detail_game: dict) -> Tuple[str]:
        headers["reviews_name"] = detail_game["title"]

        path_detail = f'{self.create_dir(raw_data=headers, main_path="data")}/detail/{Dekimashita.vdir(detail_game["title"])}.json'

        headers.update({
            "id": detail_game["id"],
            "detail_applications": detail_game,
            "path_data_raw": path_detail,
            "path_data_clean": convert_path(path_detail)
        })

        File.write_json(path_detail, headers)
        return (path_detail, headers)
        