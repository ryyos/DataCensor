
from pyquery import PyQuery
from requests import Response
from typing import Generator
from icecream import ic

from components import JihadimalmoComponent
from ApiRetrys import ApiRetry

class JihadimalmoLibs(JihadimalmoComponent):
    def __init__(self) -> None:
        super().__init__()

        self.api = ApiRetry(show_logs=True, defaulth_headers=True)
        ...

    def collect_years(self, html: PyQuery) -> Generator[str, any, None]:

        for side in html.find('#BlogArchive1_ArchiveList > ul > li > a.post-count-link'):

            year: str = PyQuery(side).text()
            url: str = PyQuery(side).attr('href')

            yield (year, url)
            ...
        ...

    def collect_months(self, url: str) -> Generator[str, any, None]:
        response: Response = self.api.get(url)
        html = PyQuery(response.text)
        ...