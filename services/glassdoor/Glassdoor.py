import os

from pyquery import PyQuery
from library import GlassdorLibs
from time import time
from icecream import ic

from utils import *

class Glassdor:
    def __init__(self) -> None:

        self.MAIN_URL = 'https://www.glassdoor.com'
        self.DOMAIN = 'www.glassdoor.com'

        self.__glassdor = GlassdorLibs()
        ...

    def main(self) -> None:

        url = 'https://www.glassdoor.com/Reviews/index.htm'
        while True:
            companies = self.__glassdor.collect_companies(url)
            break
        ...