import os
import shutil

from icecream import ic
from typing import Dict
from utils import *

class FourSharedShere:
    def __init__(self) -> None:

        self.PATH_DATA = 'data/data_raw/admiralty/four_shared/'
        self.NEW_PATH = 'data/hehe/'
        ...
    
    def create_dir(self, path: str) -> None:
        try: os.makedirs(path)
        except Exception: ...

    def change_path(self, data: Dict[str, any]) -> Dict[str, any]:

        file_name: str = data["path_data_raw"].split('/')[-1]
        file_format: str = data["path_data_raw"].split('/')[-2]

        new_path: str = self.NEW_PATH+file_format
        # self.create_dir(new_path)

        path = f'{new_path}/{file_name}'
        ic(path)

        ...

    def main(self) -> None:
        for dir in File.list_dir(self.PATH_DATA):

            ic(dir)
            if 'json' in dir:

                for file in File.list_dir(self.PATH_DATA+dir):

                    path = f'{self.PATH_DATA}{dir}/{file}'
                    # data = File.read_json(path)
                    # self.change_path(data)

                    # --> setelah update path langsung di kirim ke s3
                    
            else:

                for file in File.list_dir(self.PATH_DATA+dir):
                    old_path = f'{self.PATH_DATA+dir}/{file}'
                    new_path = f'{self.NEW_PATH+dir}/{file}'

                    shutil.copy(old_path, new_path)

                ...
                    
        ...