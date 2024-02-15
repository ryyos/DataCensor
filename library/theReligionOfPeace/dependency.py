
from typing import Generator, Tuple
from icecream import ic
from requests import Response
from pyquery import PyQuery

from ApiRetrys import ApiRetry
from components import TheReligionOfPeaceComponent

class TheReligionOfPeaceLibs(TheReligionOfPeaceComponent):
    def __init__(self) -> None:
        super().__init__()

        self.api = ApiRetry(
            show_logs=True,
            defaulth_headers=True
        )
        ...
    ...


    def collect_year(self, url: str) -> Generator[Tuple[str], any, None]:
        response: Response = self.api.get(url=url, max_retries=30)
        html = PyQuery(response.text)

        for side in html.find('table[class="tableattacks"] tr a'):

            year: str = PyQuery(side).text()
            url: str = self.base_url+PyQuery(side).attr('href')

            yield (year, url)
            
        ...