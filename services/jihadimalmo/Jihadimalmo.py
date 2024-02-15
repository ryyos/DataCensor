
from requests import Response
from icecream import ic
from pyquery import PyQuery
from typing import Tuple
from concurrent.futures import ThreadPoolExecutor, wait

from library import JihadimalmoLibs
from dekimashita import Dekimashita
from utils import *

class Jihadimalmo(JihadimalmoLibs):
    def __init__(self, s3: bool, save: bool, thread: bool) -> None:
        super().__init__(save, s3)
        self.executor = ThreadPoolExecutor()

        self.SAVE_TO_S3 = s3
        self.SAVE_TO_LOKAL = save
        self.USING_THREADS = thread
        ...

    def extract_blog(self, component: Tuple[str]) -> None:
        
        (year, month, title, url) = component

        temp_path: str = f'{self.path+year}/{month}/json'
        json_path: str = f'{create_dir(paths=temp_path, create=self.SAVE_TO_LOKAL)}/{Dekimashita.vdir(title)}.json'

        results = {
            "link": url,
            "tags": [self.domain],
            "domain": self.domain,
            "crawling_time": now(),
            "crawling_time_epoch": epoch(),
            "path_data_raw": self.s3_path+json_path,
            "path_data_clean": self.s3_path+convert_path(json_path),
            "path_data_media": [],
            "article": self.get_detail(url)
        }

        results: dict = self.downloader(headers=results, year=year, month=month)

        if self.SAVE_TO_LOKAL:
            File.write_json(json_path, results)
        
        if self.SAVE_TO_S3:

            self.s3.upload(
                key=json_path,
                body=results,
                bucket=self.bucket
            )



    def main(self) -> None:
        response: Response = self.api.get(self.main_url)
        html = PyQuery(response.text)

        for nth, (year, url) in enumerate(self.collect_years(html)):

            for month, url in self.collect_months(url=url, nth=nth+1):
                
                task_executor = []
                for blog, url in self.collect_blogs(url=url):

                    if self.USING_THREADS:
                        task_executor.append(self.executor.submit(self.extract_blog, (year, month, blog, url)))
                    else: 
                        self.extract_blog((year, month, blog, url))
                    ...
                wait(task_executor)
                ...

            ...

        self.executor.shutdown(wait=True)
        ...