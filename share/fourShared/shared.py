import os
import shutil

from icecream import ic
from typing import Dict
from server.s3 import ConnectionS3
from typing import Tuple
from dotenv import load_dotenv
from utils import *

class FourSharedShere:
    def __init__(self) -> None:
        load_dotenv()

        self.PATH_DATA = 'data/data_raw/admiralty/four_shared/'
        self.NEW_PATH = 'data/data_raw/hehe/'
        self.S3_PATH = 'S3://ai-pipeline-statistics/'

        self.__s3 = ConnectionS3(access_key_id=os.getenv('ADMIRALTY_ACCESS_KEY_ID'),
                                 secret_access_key=os.getenv('ADMIRALTY_SECRET_ACCESS_KEY'),
                                 endpoint_url=os.getenv('ADMIRALTY_ENDPOINT'),
                                 )

        self.bucket = os.getenv('ADMIRALTY_BUCKET')
        ...
    
    def create_dir(self, path: str) -> None:
        try: os.makedirs(path)
        except Exception: ...

    def change_path(self, data: Dict[str, any]) -> Tuple[Dict[str, any], str]:

        file_name: str = data["path_data_raw"].split('/')[-1]
        file_format: str = data["path_data_raw"].split('/')[-2]

        document_name: str = data["path_data_document"].split('/')[-1]
        document_format: str = data["path_data_document"].split('/')[-2]

        new_path: str = self.NEW_PATH+file_format
        new_document_path: str = self.NEW_PATH+document_format

        path = f'{new_path}/{file_name}'
        document_path = f'{new_document_path}/{document_name}'

        ic(path)
        
        data.update({
            "path_data_raw": self.S3_PATH+path,
            "path_data_clean": self.S3_PATH+convert_path(path),
            "path_data_document": self.S3_PATH+document_path
        })

        return (data, path)

        ...

    def main(self) -> None:
        for dir in File.list_dir(self.PATH_DATA):

            if 'json' in dir:

                for file in File.list_dir(self.PATH_DATA+dir):

                    source_path = f'{self.PATH_DATA}{dir}/{file}'

                    data = File.read_json(source_path)
                    
                    (data, destination) = self.change_path(data)

                    # --> setelah update path langsung di kirim ke s3

                    response = self.__s3.upload(
                                body=data,
                                key=destination,
                                bucket=self.bucket
                            )
                    
            else:

                for file in File.list_dir(self.PATH_DATA+dir):
                    source_path = f'{self.PATH_DATA+dir}/{file}'
                    new_path = f'{self.NEW_PATH+dir}/{file}'

                    # shutil.copy(source_path, new_path)

                    response = self.__s3.upload_file(
                                bucket=self.bucket,
                                key=new_path,
                                path=source_path
                            )

                ...
                    
        ...