
from typing import List
from icecream import ic
from requests import Response
from pyquery import PyQuery

from utils import *

class SoftonicLibs:
    def __init__(self) -> None:
        self.__api = ApiRetry()

        self.API_REVIEW = 'https://disqus.com/api/3.0/threads/listPostsThreaded'
        self.API_KEY = 'E8Uh5l5fHZ6gD8U3KycjAIAk46f68Zw7C6eW8WSjZvCLXebZ7p0r1yrYDrLilk2F'
        self.DISQUS_API_COMMENT = 'https://disqus.com/embed/comments'
        ...
        
    def collect_categories(self, url: str) -> List[str]:
        response: Response = self.__api.retry(url=url, action='get')
        html = PyQuery(response.text)

        categories_urls = [PyQuery(categories).attr('href') for categories in html.find('#sidenav-menu a[class="menu-categories__link"]')]
        
        return categories_urls
        ...

    def collect_games(self, url: str):
        response = self.__retry(url=url)
        
        games = []
        page = 1
        while True:
            html = PyQuery(response.text)

            for game in html.find('a[data-meta="app"]'): games.append(PyQuery(game).attr('href'))

            response: Response = self.__retry(url=f'{url}/{page}')

            if page > 1 and response.history: break

            logger.info(f'page: {page}')
            logger.info(f'total application: {len(games)}')
            print()

            page+=1

            if response.status_code != 200: break
            if not html.find('a[data-meta="app"]'): break

        return games
        ...
    

    def __param_second_cursor(self, cursor: str, thread: str) -> str:

        return f'https://disqus.com/api/3.0/threads/listPostsThreaded?limit=50&thread={thread}&forum=en-softonic-com&order=popular&cursor={cursor}&api_key={self.API_KEY}'
        ...


    def __build_param_disqus(self, url_apk: str, name_apk: str) -> str:
        return f'{self.DISQUS_API_COMMENT}/?base=default&f=en-softonic-com&t_u={url_apk}/comments&t_d={name_apk}&s_o=default#version=cb3f36bfade5c758ef967a494d077f95'
        ...