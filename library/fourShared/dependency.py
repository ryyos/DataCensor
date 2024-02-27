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
from dotenv import load_dotenv

from server.s3 import ConnectionS3
from components import FourSharedAsset
from utils import *

class FourSharedLibs(FourSharedAsset):
    def __init__(self, save: bool, s3: bool) -> None:
        super().__init__()
        load_dotenv()

        self.api = ApiRetry(show_logs=True, defaulth_headers=True)
        self.s3 = ConnectionS3(access_key_id=os.getenv('ACCESS_KEY_ID'),
                                 secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
                                 endpoint_url=os.getenv('ENDPOINT'),
                                 )

        self.bucket = os.getenv('BUCKET')

        self.api = ApiRetry(show_logs=True)
        self.executor = ThreadPoolExecutor()
        self.browser: BrowserContext = SyncPlaywright.browser(headless=True)

        self.SAVE_TO_LOKAL = save
        self.SAVE_TO_S3 = s3

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
            return (size, posted.strip(), types.strip())
        
        except Exception:
            size = (html.find('div.id3tag:nth-child(2)').text() or html.find('span[class="jsFileSize"]').text())
            posted = (html.find('div[class="generalUsername clearFix"] > span').text() or html.find('span[class="jsUploadTime"]').text())
            types = html.find('div.id3tag:first-child').text()

            return (size.strip(), posted.strip(), ' '.join(types.split(' ')[-1]).strip())
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

    def download(self, html: PyQuery, header: Dict[str, any], folder: str) -> Dict[str, any]:

        url: str = html.find('#btnLink').attr('href')

        if not url:
            url = html.find('input[class="jsDLink"]').attr('value')

        response = self.api.get(url)
        html = PyQuery(response.text)

        url_document: str = html.find('input[name="d3link"]').attr('value')
        
        ic(url_document)
        
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
        

        if self.SAVE_TO_LOKAL:
            File.write_byte(
                path=path_document,
                media=response
            )

        if self.SAVE_TO_S3:
            self.s3.upload_byte(
                body=response.content,
                bucket=self.bucket,
                key=path_document
            )

        return header
        ...

    def collect_card(self, html: PyQuery) -> Generator[str, any, None]:

        for card in html.find('div[class="hideLong simpleTumbName"] a') or html.find('a[target="_top"]')[1:] or html.find('div[class="namePlus"] a')[1:]:
            yield PyQuery(card).attr('href')

        ...


    


# data/admiralty/four_shared/json/title.json
# data/admiralty/four_shared/pdf/file.pdf