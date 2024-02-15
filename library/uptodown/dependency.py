import requests
import os

from ApiRetrys import ApiRetry
from dekimashita import Dekimashita
from requests import Response
from pyquery import PyQuery
from fake_useragent import FakeUserAgent
from icecream import ic
from typing import List
from dotenv import load_dotenv

from components import codes, UptodowndComponent
from server.s3 import ConnectionS3
from utils import *

class UptodownLibs(UptodowndComponent):
    def __init__(self) -> None:
        super().__init__()
        load_dotenv()

        self.bucket = os.getenv('BUCKET')
        
        self.faker = FakeUserAgent()
        self.parser = Parser()

        self.api = ApiRetry(
            show_logs=True, 
            handle_forbidden=True, 
            redirect_url='https://id.uptodown.com/')
        
        self.logs = Logs(
            path_monitoring='logs/uptodown/monitoring_data.json',
            path_log='logs/uptodown/monitoring_logs.json',
            domain='id.uptodown.com')

        self.s3 = ConnectionS3(
            access_key_id=os.getenv('ACCESS_KEY_ID'),
            secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
            endpoint_url=os.getenv('ENDPOINT'))


        ...

    def collect_types(self, url_platform: str) -> List[str]:
        ic(url_platform)
        response: Response = self.api.get(url=url_platform, headers=self.headers)
        ic(response)
        html = PyQuery(response.text)

        types: List[str] = []

        for type in html.find('#main-left-panel-ul-id > div:nth-child(3) div[class="li"] > a'):
            types.append(PyQuery(type).attr('href'))

        return types
        ...

    def selection_app(self, app: str) -> bool:
        pieces = PyQuery(app).attr('href').split('/')
        if self.DOMAIN in pieces: return False
        else: return True
        ...

    def collect_apps(self, url_type: str) -> List[str]:
        response: Response = self.api.get(url=url_type, headers=self.headers)
        ic(response)
        html = PyQuery(response.text)

        apps: List[str] = []

        for app in html.find('div[class="name"] > a'):
            if self.selection_app(app): apps.append(PyQuery(app).attr('href'))

        return apps
        ...

    def filter_total_review(self, text: str) -> int:
        try: return int(text.strip().split(' ')[0])
        except Exception: return None
        ...

    def filter_rating(Self, text: str) -> float:
        try: return float(text.strip())
        except Exception: return None
        ...

    def strip(self, text: str) -> str:
        try: return text.strip().replace('\n', '')
        except Exception: return text
        ...

    def selection_url(self, raw_url: str) -> str:
        try:
            pieces = raw_url.split('/')
            pieces.pop()
            return '/'.join(pieces)
        except Exception:
            return raw_url
        ...

    def handler(self, func: any, review: any, selector: str, xitem: str) -> any:
        try:
            contain: str = func.ex(review, selector).text()
            if xitem.lower() not in contain.lower(): return int(contain)
            else: return 0
        except Exception: return 0
        ...

    def create_dir(self, header: dict, component: dict) -> str:
        try: os.makedirs(f'data/data_raw/data_review/uptodown/{component["platform"]}/{component["type"]}/{Dekimashita.vdir(header["reviews_name"].lower())}/json/detail')
        except Exception: ...
        finally: return f'data/data_raw/data_review/uptodown/{component["platform"]}/{component["type"]}/{Dekimashita.vdir(header["reviews_name"].lower())}/json'
        ...

    def get_reply(self, url_app: str, id: int) -> List[str]:
        api_reply = f'{self.selection_url(url_app)}/v2/comment/{id}'
        ic(api_reply)
        response = self.api.get(url=api_reply, headers=self.headers)

        replies = PyQuery(response.json()['content'])

        all_reply: List[str] = []
        for reply in replies.find('div[class="comment answer"]'):
            all_reply.append({
                "username_reply_reviews": PyQuery(reply).find('a.user').text(),
                "content_reviews": PyQuery(reply).find('div > p').text()
            })

        return all_reply
        ...

    def get_next_review(self, url_app: str, id_app: str) -> List[dict]:

        offset = 10
        all_reviews: List[dict] = []
        error: List[dict] = []

        while True:
            response: Response = self.api.get(url=f'{url_app}/mng/v2/app/{id_app}/comments/unixtime?offset={offset}', headers=self.headers)
            if response.json()["success"] != 1: break

            offset+=10
            all_reviews.extend(response.json()['data'])

            if response.status_code != 200:
                error.append({
                    "message": response.text,
                    "type": codes[str(response.status_code)],
                    "id": None
                })

        return {
            "all_reviews": all_reviews,
            "error": error
        }
        ...