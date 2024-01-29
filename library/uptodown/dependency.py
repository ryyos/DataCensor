import requests

from ApiRetrys import ApiRetry
from requests import Response
from pyquery import PyQuery
from fake_useragent import FakeUserAgent
from icecream import ic
from typing import List

class UptodownLibs:
    def __init__(self) -> None:

        self.api = ApiRetry(show_logs=True, handle_forbidden=True, redirect_url='https://id.uptodown.com/')
        self.faker = FakeUserAgent()

        self.headers = {
            'authority': 'uptodown-android.id.uptodown.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,id;q=0.8',
            # 'cookie': 'utd_red_lang=menu',
            'referer': 'https://uptodown-android.id.uptodown.com/android',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

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

    def collect_apps(self, url_type: str) -> List[str]:
        ...