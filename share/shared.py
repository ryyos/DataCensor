import os
import shutil

from icecream import ic
from typing import Dict
from server.s3 import ConnectionS3

from dotenv import load_dotenv
from utils import *

class Share:
    def __init__(self, base_path: str) -> None:
        load_dotenv()

        self.base_path = base_path

        self.s3 = ConnectionS3(access_key_id=os.getenv('ACCESS_KEY_ID'),
                                 secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
                                 endpoint_url=os.getenv('ENDPOINT'),
                                 )

        self.bucket = os.getenv('BUCKET')
        ...

    def main(self):
        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                file_path = os.path.join(root, file).replace('\\', '/')
                
                Runtime.share(file_path)

                self.s3.upload_file(
                    path=file_path,
                    bucket=self.bucket,
                    key=file_path
                )