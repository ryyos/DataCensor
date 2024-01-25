import os
from .corrector import vname

def create_dir(main_path: str, result: dict) -> str:
    try: os.makedirs(f'{main_path}/data_raw/uptodown/{result["detail_application"]["platform"]}/{result["type"]}/{vname(result["reviews_name"].lower())}/json/detail')
    except Exception: ...
    finally: return f'{main_path}/data_raw/uptodown/{result["detail_application"]["platform"]}/{result["type"]}/{vname(result["reviews_name"].lower())}/json'
    ...

def convert_path(path: str) -> str:
    
    path = path.split('/')
    path[1] = 'data_clean'
    return '/'.join(path)
    ...