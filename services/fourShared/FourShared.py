import requests
from urllib import request

from library import FourSharedLibs
from icecream import ic

url = 'https://dc601.4shared.com/download/1VEFZFf8/Islam_Denounces_Terrorism.pdf?tsid=20240207-101049-91cebb6b&sbsr=dd1c29d0ab4bea62707bb7234db51aacb06&bip=MTgyLjIuMTQ1LjA&lgfp=30'


def curl(url: str, path: str):

    image = requests.get(url=url, headers=headers, cookies=cookies)
    ic(image)
    with open(path, 'wb') as f:
        f.write(image.content)

curl(url, 'private/44.pdf')

class FourShared(FourSharedLibs):
    def __init__(self) -> None:
        super().__init__()
    
    def main(self) -> None:
        ...
