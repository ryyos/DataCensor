
from pyquery import PyQuery
from requests import Response
from ApiRetrys import ApiRetry
from typing import Dict, List
from icecream import ic
from dekimashita import Dekimashita

from components import DanamonComponent

class DanamonLibs(DanamonComponent):
    def __init__(self) -> None:
        super().__init__()

        self.api = ApiRetry(show_logs=True, defaulth_headers=True)
        ...

    def extract_education(self, html: PyQuery) -> None:
        education: str =  '\n'.join([PyQuery(li).text().replace('\n', '') for li in html.find('#content-page li')])

        if not education:
            education_experience = False

            bios: List[str] = [PyQuery(bio) for bio in html.find('#content-page').children()]
            for bio in bios:

                ic(Dekimashita.vtext('Kualifikasi/ Latar Belakang Pendidikan').replace(' ', '') in Dekimashita.vtext(PyQuery(bio).text()).replace(' ', ''))

                if Dekimashita.vtext('Kualifikasi/ Latar Belakang Pendidikan').replace(' ', '') in Dekimashita.vtext(PyQuery(bio).text().replace(' ', '')):
                    education_experience = True
                    ic(education_experience)

                elif education_experience:
                    education: str = PyQuery(bio).text()
                    ic(education)
                    education_experience = False
                    ...

        return education
        ...

    def extract_bio(self, html: PyQuery) -> None:
        bios: List[str] = [PyQuery(bio) for bio in html.find('#content-page').children()]

        work_experience = False
        dll_status = False

        carrers: List[str] = []
        dll: str | None = None

        for bio in bios:

            if 'Pengalaman Kerja' in PyQuery(bio).text():
                
                work_experience = True
                carrers: List[str] = []

            elif PyQuery(bio).is_('p') and work_experience:
                carrers.append(PyQuery(bio).text().replace('\n', ''))

            if 'Tugas dan Tanggung Jawab' in PyQuery(bio).text():
                dll_status = True
                dll: str | None = None

            elif dll_status and not dll:
                dll: str = PyQuery(bio).text()

        return ('\n'.join(carrers), dll)
        ...

    def extract(self, url: str) -> Dict[str, str]:
        response: Response = self.api.get(url)
        html = PyQuery(response.text)

        (carrers, dll) = self.extract_bio(html)
        return {
            "nama_lengkap": html.find('div.name').text(),
            "nama_jabatan": html.find('#content-page div.title').text(),
            "riwayat_pendidikan": self.extract_education(html),
            "riwayat_pekerjaan": carrers,
            "link_foto": self.base_url+html.find('#content-page img').attr('src'),
            "biografi": html.find('div.teaser').text(),
            "riwayat_pencapaian": None,
            "tempat_tanggal_lahir": None,
            "organisasi": None,
            "dll": dll
            }
        ...