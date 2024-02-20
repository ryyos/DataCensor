import os
from dekimashita import Dekimashita
from icecream import ic


# def create_dir(headers: dict, website: str) -> str:
#     try: os.makedirs(f'data/data_raw/data_review/{website}/{Dekimashita.vdir(headers["reviews_name"].lower())}/json/detail')
#     except Exception: ...
#     finally: return f'data/data_raw/data_review/{website}/{Dekimashita.vdir(headers["reviews_name"].lower())}/json'
#     ...

def create_dir(paths: str, create: bool = True) -> str:
    try: 
        if create: os.makedirs(paths)
    except Exception as err: ...
    finally: return paths
    ...

def convert_path(path: str) -> str:
    
    path = path.split('/')
    path[1] = 'data_clean'
    return '/'.join(path)
    ...
