import os

from pyquery import PyQuery
from library import MisterAladinLibs
from time import time
from icecream import ic

from utils import *

class MisterAladin:
    def __init__(self) -> None:

        self.MAIN_URL = 'https://www.misteraladin.com/'
        self.DOMAIN = 'www.misteraladin.com'

        self.__aladin = MisterAladinLibs()
        ...

    def main(self) -> None:
        
        city = 0
        while True:
            hotels = self.__aladin.collect_hotels('https://www.misteraladin.com/hotel/city/14/')

            ic(hotels)
            break
