
from icecream import ic
from requests import Response
from pyquery import PyQuery

from library import TheReligionOfPeaceLibs
from dekimashita import Dekimashita
from utils import *

class TheReligionOfPeace(TheReligionOfPeaceLibs):
    def __init__(self, stream: bool, all: bool, save: bool, path: str) -> None:
        super().__init__()

        self.stream: bool = stream
        self.all: bool = all

        self.save: bool = save
        self.path: str = path
        ...

    def get_all(self, url: str, year: str) -> None:
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
            "table": self.extract_table(html)
        }

        if self.save:
            if not self.path: raise FileNotFoundError

            path: str = self.path+year
            path: str = create_dir(path)

            ic(path)

            File.write_json(f'{path}/{Dekimashita.vdir(results["title"])}.json', results)
        ...

    def main(self) -> None:

        if self.all:
            for year, url in self.collect_year(self.main_url):
                self.get_all(url=url, year=year)
            ...
        ...

#  data/kafka/admiralty/theReligionOfPeace/json/