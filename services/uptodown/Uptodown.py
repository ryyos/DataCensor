
from library import UptodownLibs
from icecream import ic

class Uptodown:
    def __init__(self) -> None:

        self.__platforms = ['android', 'windows', 'mac']

        self.__MAIN_URL = 'https://id.uptodown.com/'
        self.__DOMAIN = 'id.uptodown.com'

        self.__uptodown = UptodownLibs()
        ...


    def main(self) -> None:
        for platform in self.__platforms:
            types = self.__uptodown.collect_types(self.__MAIN_URL+platform)

        for type in types:
            break

        ...
    