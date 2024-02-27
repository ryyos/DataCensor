import os
import urllib.parse

from typing import Dict
from dotenv import load_dotenv
from icecream import ic

from server.s3 import ConnectionS3
from ApiRetrys import ApiRetry
from database import SQL
from database import SQLlite
from utils import *

class DownloadLibs:
    def __init__(self, save: bool) -> None:
        load_dotenv()

        self.api = ApiRetry(show_logs=True, defaulth_headers=False)
        self.sqlite = SQLlite()

        self.s3 = ConnectionS3(access_key_id=os.getenv('ACCESS_KEY_ID'),
                                 secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
                                 endpoint_url=os.getenv('ENDPOINT'),
                                 )
        
        self.cursor = self.sqlite.connection.cursor()

        self.bucket = os.getenv('BUCKET')
        self.S3_PATH = "s3://ai-pipeline-statistics/"

        self.SAVE_TO_LOCAL: bool = save
        ...

    def get_title(self, url: str) -> str:
        decoded: str = urllib.parse.unquote(url.replace('+', ' '))
        title = decoded.split('/')[-1]
        if '?' in title:
            title = title.split('?')[0]

        return title
        ...

    def save(self, path: str, domain: str) -> str | None:

        query_check = f'SELECT path FROM path WHERE domain="{domain}";'
        query_add = f'INSERT INTO path (path, domain) VALUES ("{path}", "{domain}");'

        self.cursor.execute(query_check)

        try:
            path_in_database: str = self.cursor.fetchone()[0]

        except Exception:

            if not path: raise Exception('path not found, please insert path')
            self.cursor.execute(query_add)
            self.sqlite.connection.commit()
            self.sqlite.connection.close()

            Stream.sql_domain(domain, path)
            return path

        
        self.sqlite.connection.close()

        ic(path_in_database)
        
        return path_in_database
        ...

    def update_path(self, headers: dict, base_path: str, bucket: str, format: str) -> Dict[str, any]:

        path_domain: str = headers["domain"].split('.')[-2]
        path_title: str = headers["title"].split('.')[0]
        file_title: str = headers["title"]

        if format not in file_title:
            file_title = f'{file_title}.{format}'

        if base_path:
            base_path: str = base_path.replace('\\', '/')
            if not base_path.endswith('/'): base_path: str = base_path+'/'
            base_path = base_path+path_domain
        else:
            base_path = None

        base_path = self.save(
            path=base_path,
            domain=headers['domain']
            )
        
        document_path: str = f'{create_dir(paths=f"{base_path}/{path_title}/{format}", create=self.SAVE_TO_LOCAL)}/{file_title}'
        json_path: str = f'{create_dir(paths=f"{base_path}/{path_title}/json", create=self.SAVE_TO_LOCAL)}/{file_title.replace(format, "json")}'

        headers.update({
            "path_data_raw": bucket+json_path,
            "path_data_clean": bucket+convert_path(json_path),
            "path_data_document": bucket+document_path,
        })

        return headers

        ...