import os
import requests

from time import sleep
from typing import Dict, Tuple, List, Generator
from ApiRetrys import ApiRetry
from requests import Response
from pyquery import PyQuery
from concurrent.futures import ThreadPoolExecutor
from dekimashita import Dekimashita
from browser import SyncPlaywright, BrowserContext, Page
from icecream import ic

from components import FourSharedAsset
from utils import *

class FourSharedLibs(FourSharedAsset):
    def __init__(self, save: bool) -> None:
        super().__init__()

        self.api = ApiRetry(show_logs=True)
        self.executor = ThreadPoolExecutor()
        self.browser: BrowserContext = SyncPlaywright.browser(headless=True)

        self.SAVE_TO_LOKAL = save

        self.temp_path = None

        ...

    def update_cookies(self) -> None:
        page: Page = self.browser.new_page()

        page.goto(url=self.login)

        page.get_by_placeholder('Login').fill(self.EMAIL)
        page.get_by_role("textbox", name="Sandi").fill(self.PASS)
        page.get_by_role("button", name="Login »").click()
        sleep(10)

        for cookie in self.browser.cookies():
            self.cookies.update({
                cookie["name"]: cookie["value"]
            })
            ...

        File.write_json('private/cookies.json', self.cookies)
        page.close()
        self.browser.close()
        ...

    def extract_navbar(self, html: PyQuery) -> Tuple[str]:
        try:
            (size, posted, types, _) = html.find('p.fileInfo').text().split(' |')
            return (' '.join(size.split(' ')[1:]), posted.strip(), types.strip())
        
        except Exception:
            size = html.find('div.id3tag:nth-child(2)').text()
            posted = html.find('div[class="generalUsername clearFix"] > span').text()
            types = html.find('div.id3tag:first-child').text()

            return (' '.join(size.split(' ')[1:]).strip(), posted.strip(), ' '.join(types.split(' ')[-1]).strip())
        ...

    def create_dir(self, format: str, folder: str) -> str:
        # s3://ai-pipeline-statistics/data/data_raw/admiralty/data_radikalisme/
        path = f'data/data_raw/admiralty/data_radikalisme/4shared/{folder}/{format}'
        try:
            if self.SAVE_TO_LOKAL: os.makedirs(path)
        except Exception: ...
        finally: return path
        ...

    def collect_document(self, url: str) -> List[str]:
        response: Response = self.api.get(url='https:'+url)
        html = PyQuery(response.text)

        names: List[str] = []
        urls: List[str] = []

        for url in html.find('a[target="_top"]'):
            urls.append(PyQuery(url).attr('href'))
            names.append(PyQuery(url).text())

        return (names, urls)
        ...

    def download(self, html: PyQuery, header: Dict[str, any]) -> Dict[str, any]:

        url: str = html.find('#btnLink').attr('href')
        folder: str = html.find('a[class="gaClick hideLong"]').text()

        ic(url)
        if not url:
            url = html.find('input[class="jsDLink"]').attr('value')
        
        if not folder:
            folder: str = self.temp_path

        self.temp_path = folder

        ic(folder)

        response = self.api.get(url)
        html = PyQuery(response.text)

        url_document: str = html.find('input[name="d3link"]').attr('value')
        
        response = requests.get(url=url_document, 
                                cookies=self.cookies, 
                                headers=self.headers)
        
        sleep(20)
        
        response = requests.get(url=url_document, 
                                cookies=self.cookies, 
                                headers=self.headers)

        path_document = f'{self.create_dir(format=url_document.split("?")[0].split(".")[-1], folder=folder)}/{header["detail"]["title"].split(".")[0].replace(" ", "_")}.{url_document.split("?")[0].split(".")[-1]}'
        header.update({
            "path_data_document": self.BASE_PATH+path_document
        })
        
        with open(path_document, 'wb') as f:
            f.write(response.content)

        return header
        ...

    def collect_card(self, html: PyQuery) -> Generator[str, any, None]:

        for card in html.find('div[class="hideLong simpleTumbName"] a'):
            yield PyQuery(card).attr('href')

        ...


    


# data/admiralty/four_shared/json/title.json
# data/admiralty/four_shared/pdf/file.pdf