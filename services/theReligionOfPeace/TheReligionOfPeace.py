
from icecream import ic
from requests import Response
from pyquery import PyQuery

from library import TheReligionOfPeaceLibs
from dekimashita import Dekimashita
from utils import *

class TheReligionOfPeace(TheReligionOfPeaceLibs):
    def __init__(self, all: bool) -> None:
        super().__init__()

        self.all: bool = all
        ...

    def extract(self, url: str, year: str, stream: bool) -> None:
        response: Response = self.api.get(url=url, max_retries=30)
        html = PyQuery(response.text)

        results = {
            "link": url,
            "domain": self.domain,
            "tags": [self.domain],
            "topic_kafka": self.topic,
            "crawling_time": now(),
            "crawling_time_epoch": epoch(),
            "title": html.find('h2[class="h3-DarkSlate"]').text(),
            "year": self.to_int(year),
            "url_media": [self.base_url+PyQuery(img).attr('src').replace('\\', '/') for img in html.find('table[class="quran-table"] img')],
            "descriptions": self.filter(html),
            "jihad_report": self.extract_jihad(html),
            "table": self.extract_table(html, stream=stream)
        }

        if stream:
            path: str = self.path_stream+year
            path: str = f'{create_dir(path)}/{epoch()}.json'

        else:
            path: str = self.path_all+year
            path: str = f'{create_dir(path)}/{Dekimashita.vdir(results["title"])}.json'

        if results["table"]:
            File.write_json(path, results)

        Runtime.found(
            process='STREAM',
            message='DATA FOUND',
            total=len(results["table"])
        )
        ...


    def main(self) -> None:

        for year, url in self.collect_year(self.main_url):
            self.extract(url=url, year=year, stream=bool(not self.all))

            if not self.all: break
            ...