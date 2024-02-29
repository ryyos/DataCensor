
from requests import Response
from pyquery import PyQuery
from typing import Dict, List, Tuple
from icecream import ic

from library import  PermataLibs
from utils import *

class Permata(PermataLibs):
    def __init__(self) -> None:
        super().__init__()
        ...

    def main(self) -> None:
        response: Response = self.api.get(self.target_url)
        html = PyQuery(response.text)

        all_direksi = html.find('section[data-id="Direksi"]')
        all_komesaris = html.find('section[data-id="Dewan-Komisaris"]')

        for direksi, komesaris in zip(all_direksi.find('div.card-item'), all_komesaris.find('div.card-item')):
            File.write_json('private/permata.json', self.extract(PyQuery(komesaris)))
            break
            ...
        ...