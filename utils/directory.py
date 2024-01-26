import os
from .corrector import vname


def create_dir(self, headers: dict, website: str) -> str:
    try: os.makedirs(f'{self.MAIN_PATH}/data_raw/{website}/{vname(headers["reviews_name"].lower())}/json/detail')
    except Exception: ...
    finally: return f'{self.MAIN_PATH}/data_raw/{website}/{vname(headers["reviews_name"].lower())}/json'
    ...


def convert_path(path: str) -> str:
    
    path = path.split('/')
    path[1] = 'data_clean'
    return '/'.join(path)
    ...

