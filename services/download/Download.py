import requests
import mimetypes

from typing import Dict
from requests import Response
from icecream import ic

from library import DownloadLibs
from utils import *

class Download(DownloadLibs):
    def __init__(self, save: bool, s3: bool) -> None:
        super().__init__(save=save)

        self.SAVE_TO_LOCAL: bool = save
        self.SAVE_TO_S3: bool = s3
        ...

    def metadata(self, url: str, domain: str) -> Dict[str, any]:

        headers = {
            "link": url,
            "domain": domain,
            "tags": [domain],
            "crawling_time": now(),
            "crawling_time_epoch": epoch(),
            "path_data_raw": "",
            "path_data_clean": "",
            "path_data_document": "",
            "title": self.get_title(url)
        }

        return headers
        ...

    def main(self, url: str, domain: str, path: str) -> None:
        response = self.api.get(url)

        format_document: str = mimetypes.guess_extension(response.headers.get('Content-Type')).replace('.', '')

        headers: Dict[str, any] = self.metadata(url, domain)
        headers: Dict[str, any] = self.update_path(
                                        headers=headers,
                                        base_path=path,
                                        bucket=self.S3_PATH,
                                        format=format_document
                                    )
        
        json_path: str = headers["path_data_raw"].replace(self.S3_PATH, '')
        document_path: str = headers["path_data_document"].replace(self.S3_PATH, '')

        if self.SAVE_TO_LOCAL:
            File.write_json(path=json_path, content=headers)
            Down.curlv2(response=response, path=document_path)

        if self.SAVE_TO_S3:
            self.s3.upload(key=json_path, body=headers, bucket=self.bucket)
            self.s3.upload_byte(key=document_path, bucket=self.bucket, body=response.content)
        
        ...

# data/data_raw/admiralty/