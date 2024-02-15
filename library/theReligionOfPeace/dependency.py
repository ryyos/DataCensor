
from typing import Generator, Tuple, List, Dict
from icecream import ic
from requests import Response
from pyquery import PyQuery

from ApiRetrys import ApiRetry
from components import TheReligionOfPeaceComponent
from dekimashita import Dekimashita

class TheReligionOfPeaceLibs(TheReligionOfPeaceComponent):
    def __init__(self) -> None:
        super().__init__()

        self.api = ApiRetry(
            show_logs=True,
            defaulth_headers=True
        )
        ...
    ...

    def to_int(self, text: str) -> int | str:
        try:
            return int(text)
        
        except Exception:
            return text
        ...

    def collect_year(self, url: str) -> Generator[Tuple[str], any, None]:
        response: Response = self.api.get(url=url, max_retries=30)
        html = PyQuery(response.text)

        for side in html.find('table[class="tableattacks"] tr a'):

            year: str = PyQuery(side).text()
            url: str = self.base_url+PyQuery(side).attr('href')

            yield (year, url) 
        ...

    def filter(self, html: PyQuery) -> str:
        try:
            return Dekimashita.vtext(html.find('table[class="quran-table"] > tr:nth-child(2) > td').text())\
            .replace(Dekimashita.vtext(html.find('table[class="quran-table"] > tr:nth-child(2) h2').text()), '')
        except Exception:
            return None
        ...

    def extract_table(self, html: PyQuery) -> List[Dict[str, any]]:

        table = html.find('table[cellpadding="3px"]')
        header = PyQuery(table).find('tr:first-child th')

        tables = [
            {
                PyQuery(header[nth]).text() : self.to_int(PyQuery(row).text()) for nth, row in enumerate(PyQuery(column).find('td'))
            } for column in PyQuery(table).find('tr')[1:]
        ]

        return tables
        ...
        
    def get_intervals(self, text: str) -> str:
        try:
            return ' '.join(text.replace('\n', ' ').split(' ')[2:]).strip()
        except Exception: return text
        ...

    def extract_jihad(self, html: PyQuery) -> Dict[str, any]:
        
        jihads = [
            {
                key: self.to_int(PyQuery(row).find('td.tablejihadreportcellstat').text())
                for row in PyQuery(table).find('tr')
                if (key := PyQuery(row).find('td.tablejihadreportcelllabel').text())
            }
            | {"intervals": self.get_intervals(PyQuery(table).find('h3').text())}
            for table in html.find('table[class="tablejihadreport"]')
        ]

        return jihads

        ...