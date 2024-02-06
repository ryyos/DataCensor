import requests

from ApiRetrys import ApiRetry
from requests.sessions import Session
from icecream import ic
from time import sleep
from pyquery import PyQuery
from browser import Playwright
from playwright.sync_api import Page, Response
from fake_useragent import FakeUserAgent
from browser import SyncPlaywright
from typing import List

class IndeedLibs:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.api = ApiRetry(show_logs=True)
        self.seesion = Session()
        self.browser = SyncPlaywright.browser()
        self.faker = FakeUserAgent()
        self.page = self.browser.new_page()

        self.MAIN_URL = 'https://id.indeed.com'
        self.DOMAIN = 'id.indeed.com'
        self.LINK = 'https://id.indeed.com/companies/browse-companies/'
        self.ALPHABETS = ['a', 'b', ]

        self.cookies = {
            'indeed_rcc': '""',
            'CTK': '1hlunl74uiecn802',
            'INDEED_CSRF_TOKEN': 'iHaAHEjx5ZSL3VpUtXAyfGFaONuJGLsX',
            'bvcmpgn': 'id-indeed-com',
            '_cfuvid': 'QbOA7856IwLvkQA302m2zuvk.UoBhzNBF9Snh2c.08g-1707207204061-0-604800000',
            'indeed_rcc': 'CTK',
            '__cf_bm': 'aUl8ClNKp3UJrnmjo4hkdMHhYiyCg7OX7XEHdTFe2LQ-1707209761-1-Aaqy4MPEYvOU1a+GF6JgY+PB9vGpyuF/i9cgDzgYIpaqxSYqJ1FZDeWHh1reB7Q8sg5d8WlfkVV+0g8PswmvLT4=',
        }

        self.headers = {
            'authority': 'id.indeed.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9,id;q=0.8',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': self.faker.random
        }

        ...

    def update_cookies(self) -> dict[str, dict]:
        for cookie in self.browser.cookies():
            self.cookies.update({
                cookie['name']: cookie['value']
            })
        ...


    def get_companies(self, alphabet: str) ->List[str]:
        ic(self.LINK+alphabet)
        ic(self.seesion.get(url=self.LINK+alphabet, headers=self.headers, cookies=self.cookies))
        ic(self.cookies)

        self.page.goto(self.LINK+alphabet)
        self.update_cookies()
        ic(self.seesion.get(url=self.MAIN_URL, headers=self.headers, cookies=self.cookies))

        ic(self.cookies)
        ic(self.seesion.get(url=self.LINK+alphabet, headers=self.headers, cookies=self.cookies))

        return self.page.eval_on_selector_all('div[data-tn-element="CompanyUrlLink"] a', '(as) => as.map(a => a.href)')
        ...
