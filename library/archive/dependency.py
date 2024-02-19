import os
import mimetypes

from typing import List, Dict, Tuple
from requests import Response
from icecream import ic
from dotenv import load_dotenv

from ApiRetrys import ApiRetry
from pyquery import PyQuery
from components import ArchiveComponent
from server.s3 import ConnectionS3
from utils import *

class ArchiveLibs(ArchiveComponent):
    def __init__(self, save: bool, s3: bool) -> None:
        super().__init__()
        load_dotenv()

        self.api = ApiRetry(show_logs=True, defaulth_headers=True)
        self.s3 = ConnectionS3(access_key_id=os.getenv('ACCESS_KEY_ID'),
                                 secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
                                 endpoint_url=os.getenv('ENDPOINT'),
                                 )

        self.bucket = os.getenv('BUCKET')
        self.SAVE_TO_LOKAL = save
        self.SAVE_TO_S3 = s3

    def url_download_page(self, html: PyQuery) -> Tuple[str, any, None]:
        id: str = html.find('meta[property="og:url"]').attr('content').split('/')[-1]

        return (self.download_enpoint+id, id)
        ...

    def collect_documents(self, url_page: str) -> List[Dict[str, str]]:
        response: Response = self.api.get(url_page)
        html = PyQuery(response.text)

        documents: List[dict] = []
        for document in html.find('table[class="directory-listing-table"] tbody tr')[1:]:
            documents.append({
                "title": PyQuery(document).find('td:first-child a').text(),
                "url": url_page+'/'+PyQuery(document).find('td:first-child a').attr('href'),
                "last_modified": PyQuery(document).find('td:nth-child(2)').text(),
                "size": PyQuery(document).find('td:nth-child(3)').text(),
            })

            ...

        return documents
        ...

    def download(self, headers: dict) -> Dict[str, any]:

        documents: List[str] = []
        for document in headers["documents"]:
            ic(document["url"])
            response: Response = self.api.get(document["url"])

            try:
                extension: str = mimetypes.guess_extension(response.headers.get('Content-Type')).replace('.', '')
            except Exception:
                extension: str = document["url"].split('.')[-1]

            path: str = create_dir(f'{self.base_path+headers["id"]}/{extension}/', create=self.SAVE_TO_LOKAL)
            document.update({
                "path_document": self.s3_path+path+document["title"]
            })

            documents.append(document)

            if self.SAVE_TO_LOKAL:
                Down.curlv2(path+document["title"], response)

            if self.SAVE_TO_S3:
                self.s3.upload_byte(
                    body=response.content,
                    bucket=self.bucket,
                    key=path+document["title"]
                )
            ...

        path_temp: str = f'{self.base_path+headers["id"]}/json/'
        path_temp: str = f'{create_dir(path_temp, create=self.SAVE_TO_LOKAL)}{headers["id"]}.json'
        headers.update({
            "documents": documents,
            "path_data_raw": self.s3_path+path_temp,
            "path_data_clean": self.s3_path+convert_path(path_temp)
        })

        return headers
        ...