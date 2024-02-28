
from ApiRetrys import ApiRetry
from typing import List, Dict
from pyquery import PyQuery
from icecream import ic

from components import BtnComponent

class BtnLibs(BtnComponent):
    def __init__(self) -> None:
        super().__init__()

        self.api = ApiRetry(show_logs=True)
        ...

    def extract_education(self, html: PyQuery) -> str:
        return '\n'.join([PyQuery(p).text().replace('\n', '') 
                               for p in html.find('ul > li')]) 
        ...

    def extract_career(self, html: PyQuery) -> set:
        bios: List[str] = [PyQuery(bio) for bio in html.find('div:nth-child(3)').children()]

        if not len(bios) > 2: bios: List[str] = [PyQuery(bio) for bio in html.find('div:nth-child(3) > div').children()]

        under_h2 = False
        carrers: List[str] = []
        for bio in bios:

            if PyQuery(bio).is_('h2'):
                
                under_h2 = True
                carrers: List[str] = []

            elif PyQuery(bio).is_('p') and under_h2:
                carrers.append(PyQuery(bio).text().replace('\n', ''))
                ...

        return '\n'.join(carrers)
        ...

    def extract(self, html: PyQuery) -> Dict[str, any]:
        
        return {
            "nama_lengkap": html.find('h2[class="org-profile-details-name"]').text(),
            "nama_jabatan": html.find('p[class="org-profile-details-title"]').text(),
            "riwayat_pendidikan": self.extract_education(html),
            "riwayat_pekerjaan": self.extract_career(html),
            "riwayat_pencapaian": None,
            "link_foto": self.base_url+html.find('img').attr('src'),
            "tempat_tanggal_lahir": PyQuery(html.find('p[style="margin: 0px 0px 1rem;"]')).text().split(':')[-1].strip(),
            "biografi": None,
            "organisasi": None,
            "dll": None
            }
        ...

