import os
import mimetypes
import requests

from typing import List, Dict, Tuple, Generator
from requests import Response
from icecream import ic
from dotenv import load_dotenv

from concurrent.futures import ThreadPoolExecutor, wait
from ApiRetrys import ApiRetry
from pyquery import PyQuery
from components import ArchiveComponent
from server.s3 import ConnectionS3
from utils import *
from dekimashita import Dekimashita

class ArchiveLibs(ArchiveComponent):
    def __init__(self, save: bool, s3: bool, threads: bool) -> None:
        super().__init__()
        load_dotenv()

        self.executor = ThreadPoolExecutor()

        self.api = ApiRetry(show_logs=True, defaulth_headers=False)
        self.s3 = ConnectionS3(access_key_id=os.getenv('ACCESS_KEY_ID'),
                                 secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
                                 endpoint_url=os.getenv('ENDPOINT'),
                                 )

        self.bucket = os.getenv('BUCKET')
        self.SAVE_TO_LOKAL = save
        self.SAVE_TO_S3 = s3
        self.USING_THREAD: bool = threads

        self.temp_url = []

    def url_download_page(self, html: PyQuery) -> Tuple[str, any, None]:
        id: str = html.find('link[rel="canonical"]').attr('href').split('/')[-1]

        return (self.download_enpoint+id, id)
        ...

    def build_title(self, text: str, extension: str) -> str:
        text: str = text.split('.')[0].lower()
        text: str = text.replace(' ', '_')\
                    .replace('\n', '')\
                    .replace(',', '')\
                    .replace('(', '')\
                    .replace(')', '')
        
        if len(text) > 50: text: str = text[:50]
        return f'{text}.{extension}'
        ...

    def collect_documents(self, url_page: str, documents: list = []) -> List[Dict[str, str]]:
        response: Response = self.api.get(url_page)
        html = PyQuery(response.text)

        documents: List[dict] = [*documents]

        for document in html.find('table[class="directory-listing-table"] tbody tr')[1:]:
            
            try:

                if PyQuery(document).find('td:first-child a').attr('href').endswith('/'):
                    self.temp_url.append(url_page+'/'+PyQuery(document).find('td:first-child a').attr('href'))
                    continue
            
            except Exception:
                continue

            documents.append({
                "title": PyQuery(document).find('td:first-child a').text(),
                "url": url_page+'/'+PyQuery(document).find('td:first-child a').attr('href'),
                "last_modified": PyQuery(document).find('td:nth-child(2)').text(),
                "size": PyQuery(document).find('td:nth-child(3)').text(),
            })
        
            ...

        if self.temp_url:
            for url_page in self.temp_url:
                self.collect_documents(self.temp_url.pop(0), documents)

        return documents
        ...
    def action(self, components: Tuple) -> Dict[str, any]:

        (document, headers) = components
        response: Response = self.api.get(document["url"])

        try:
            extension: str = document["url"].split('.')[-1].lower()
        except Exception:
            extension: str = mimetypes.guess_extension(response.headers.get('Content-Type')).replace('.', '').lower()

        path: str = create_dir(f'{self.base_path+headers["id"]}/{extension}/', create=self.SAVE_TO_LOKAL)
        ic(path)
        document.update({
            "path_document": self.s3_path+path+self.build_title(document["title"], extension)
        })

        if self.SAVE_TO_LOKAL:
            path_media: str = path+self.build_title(document["title"], extension)
            Down.curlv2(path_media, response)
            

        if self.SAVE_TO_S3:
            self.s3.upload_byte(
                body=response.content,
                bucket=self.bucket,
                key=path+self.build_title(document["title"], extension)
            )

        return document

        ...

    def download(self, headers: dict) -> Dict[str, any]:

        documents: List[str] = []
        task_executor: List[str] = []

        for document in headers["documents"]:
            components = (document, headers)

            if self.USING_THREAD:
                task_executor.append(self.executor.submit(self.action, components))
            
            else:
                documents.append(self.action(components))

            ...
        
        if self.USING_THREAD:

            wait(task_executor)
            for task in task_executor:
                documents.append(task.result())
            

        path_temp: str = f'{self.base_path+headers["id"]}/json/'
        path_temp: str = f'{create_dir(path_temp, create=self.SAVE_TO_LOKAL)}{headers["id"]}.json'
        headers.update({
            "documents": documents,
            "path_data_raw": self.s3_path+path_temp,
            "path_data_clean": self.s3_path+convert_path(path_temp)
        })

        return headers
        ...

    def update_param(self, page: int) -> Dict[str, str]:
        self.params.update({
            "page": str(page+1),
            "client_url": self.client_url+str(page)
        })

        return self.params
        ...

    def collect_card(self, url: str) -> Generator[str, any, None]:
        page = 0
        while True:
            response = self.api.get(
                    'https://archive.org/services/search/beta/page_production/',
                    params=self.update_param(page),
                    cookies=self.cookies,
                    headers=self.headers,
                )

            if response.status_code != 200: break
            
            for data in response.json()['response']['body']['hits']['hits']:
                yield self.detail_endpoint+data['fields']['identifier']

            page+=1
            ...
        ...

    def get_name_page(self, url: str) -> str:
        self.base_path = self.base_path+url.split('/')[4]+'/'
        ...