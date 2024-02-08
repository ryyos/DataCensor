import requests
from urllib import request

from library import FourSharedLibs
from icecream import ic

class FourShared(FourSharedLibs):
    def __init__(self) -> None:
        super().__init__()
        ...

    
    def main(self) -> None:
        self.extract_header(self.link)
        ...
