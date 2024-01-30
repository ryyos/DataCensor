import os

from ApiRetrys import ApiRetry
from icecream import ic

from utils import *

class MisterAladinLibs:
    def __init__(self) -> None:

        self.api = ApiRetry(show_logs=True, defaulth_headers=False, redirect_url='https://www.misteraladin.com/')
        ...
