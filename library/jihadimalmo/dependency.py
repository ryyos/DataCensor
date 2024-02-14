import os
import mimetypes

from pyquery import PyQuery
from requests import Response
from typing import Generator, Dict
from icecream import ic
from dotenv import load_dotenv

from server.s3 import ConnectionS3
from components import JihadimalmoComponent
from ApiRetrys import ApiRetry
from dekimashita import Dekimashita
from utils import *

class JihadimalmoLibs(JihadimalmoComponent):
    def __init__(self, save: bool, s3: bool) -> None:
        super().__init__()

        self.api = ApiRetry(show_logs=True, defaulth_headers=True)

        self.s3 = ConnectionS3(access_key_id=os.getenv('ACCESS_KEY_ID'),
                                 secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
                                 endpoint_url=os.getenv('ENDPOINT'),
                                 )

        self.bucket = os.getenv('BUCKET')
        self.SAVE_TO_LOKAL = save
        self.SAVE_TO_S3 = s3
        ...

    def correct(self, url: str) -> str:
        if 'https:' not in url:
            return 'https:'+url
        
        return url
        ...

    def collect_years(self, html: PyQuery) -> Generator[str, any, None]:

        for side in html.find('#BlogArchive1_ArchiveList > ul > li > a.post-count-link'):

            year: str = PyQuery(side).text()
            url: str = PyQuery(side).attr('href')

            yield (year, url)
            ...
        ...

    def collect_months(self, url: str, nth: int) -> Generator[str, any, None]:
        response: Response = self.api.get(url)
        html = PyQuery(response.text)

        for side in html.find(f'#BlogArchive1_ArchiveList > ul:nth-child({nth}) > li > ul > li > a.post-count-link'):
            
            month: str = PyQuery(side).text()
            url: str = PyQuery(side).attr('href')

            yield (month, url)
            ...
        ...

    def collect_blogs(self, url: str) -> Generator[str, any, None]:
        response: Response = self.api.get(url)
        html = PyQuery(response.text)

        for side in html.find('#BlogArchive1_ArchiveList ul[class="posts"] > li a'):

            blog: str = PyQuery(side).text()
            url: str = PyQuery(side).attr('href')

            yield (blog, url)
        ...

    def get_detail(self, url: str) -> Dict[str, any]:
        response: Response = self.api.get(url)
        html = PyQuery(response.text)

        detail = {
            "title": html.find('h3[class="post-title entry-title"]').text(),
            "posted": html.find('h2[class="date-header"]').text(),
            "aticle": Dekimashita.vdict(html.find('div[itemprop="description articleBody"]').text(), chars=['\n']),
            "media": [self.correct(PyQuery(img).attr('src')) for img in html.find('div[itemprop="blogPost"] img')[:1]],
            "populer": [
                {
                    "url": PyQuery(blog).find('div[class="item-title"] a').attr('href'),
                    "title": PyQuery(blog).find('div[class="item-title"]').text(),
                    "thumbnail": PyQuery(blog).find('div[class="item-thumbnail"] a').attr('href'),
                    "description": PyQuery(blog).find('div[class="item-snippet"]').text()
                } for blog in html.find('div.popular-posts')
            ],
            "urls": [PyQuery(url).attr('href') for url in html.find('div[class="widget LinkList"] a')]
        }

        return detail
        ...

    def downloader(self, headers: dict, **kwargs) -> Dict[str, any]:

        try:
            ic(headers["article"]["media"])
            for url in headers["article"]["media"]:
                
                response: Response = self.api.get(url)
                extension: str = mimetypes.guess_extension(response.headers.get('Content-Type')).replace('.', '')

                temp_path: str = f'{self.path+kwargs["year"]}/{kwargs["month"]}/{extension}'
                path_media: str = f'{create_dir(paths=temp_path, create=self.SAVE_TO_LOKAL)}/{epoch_ms()}.{extension}'

                if self.SAVE_TO_LOKAL: 
                    Down.curlv2(path=path_media, response=response)
                headers["path_data_media"].append(self.s3_path+path_media)

                if self.SAVE_TO_S3:
                    self.s3.upload_byte(
                        body=response.content,
                        key=path_media,
                        bucket=self.bucket
                    )
                ...
        except Exception: ...

        finally: return headers
        ...