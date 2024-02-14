import os
import shutil

from icecream import ic
from typing import Dict
from server.s3 import ConnectionS3
from typing import Tuple
from dotenv import load_dotenv
from utils import *

class ShareV2:
    def __init__(self) -> None:
        load_dotenv()

        self.S3_PATH = 'S3://ai-pipeline-statistics/'

        self.s3 = ConnectionS3(access_key_id=os.getenv('ACCESS_KEY_ID'),
                                 secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
                                 endpoint_url=os.getenv('ENDPOINT'),
                                 )

        self.bucket = os.getenv('BUCKET')
        ic(self.bucket)
        ...
    
    def create_dir(self, path: str) -> None:
        try: os.makedirs(path)
        except Exception: ...

    def change_path(self, data: Dict[str, any], new_path: str, start_main_path: int) -> Tuple[Dict[str, any], str]:

        main_path: str = '/'.join(data["path_data_raw"].split('/')[start_main_path:])
        main_document_path: str = '/'.join(data["path_data_document"].split('/')[start_main_path:])

        new_path: str = new_path+main_path
        new_document_path: str = new_path + main_document_path
        
        data.update({
            "path_data_raw": self.S3_PATH+new_path,
            "path_data_clean": self.S3_PATH+convert_path(new_path),
            "path_data_document": self.S3_PATH+new_document_path
        })

        return (data, new_path)
        ...

    def change_document_path(self, source_path: str, new_path: str, start_main_path: int) -> str:

        main_path: str = '/'.join(source_path[start_main_path:])

        return new_path+main_path
        ...

    def main(self, source: str, new_path: str = None, change_path: bool = False, start_main_path: int = None) -> None:
        """
        Use:
            python shared.py 
        Note:
            selalu akhiri path dengan /
        Param:
            change_path (bool): merubah path atau tidak
            source (str): path asal document
            new_path (str): path baru
            start_main_path (int): index mulai path utama

                ex:
                data/data_raw/admiralty/data_radikalisme/presiden_2024/json/prabowo.json

                path utama -> presiden_2024/json/prabowo.json
                path yang akan di ganti -> data/data_raw/admiralty/data_radikalisme/
                berarti start_main_path nya -> 3

        Returns:
            (data, new_path)
        """

        for dir in File.list_dir(source):

            if 'json' in dir:

                for file in File.list_dir(source+dir):

                    # Jika tidak merubah path source path dan path ke s3 akan sama
                    source_path: str = f'{source+dir}/{file}'

                    data: dict = File.read_json(source_path)
                    
                    if change_path:
                        (data, destination) = self.change_path(data)
                    
                    else:
                        destination: str = source_path


                    # --> setelah update path langsung di kirim ke s3
                    response: int = self.s3.upload(
                                body=data,
                                key=destination,
                                bucket=self.bucket
                            )
                    
            else:

                for file in File.list_dir(source+dir):

                    # Jika tidak merubah path source path dan path ke s3 akan sama
                    source_path: str = f'{source+dir}/{file}'

                    if change_path:
                        new_path = self.change_document_path(
                            source_path=source_path,
                            new_path=new_path,
                            start_main_path=start_main_path)
                        
                    else:
                        new_path: str = source_path

                    response: int = self.s3.upload_file(
                                bucket=self.bucket,
                                key=new_path,
                                path=source_path
                            )

                ...
                    
        ...