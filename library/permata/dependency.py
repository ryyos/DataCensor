
from ApiRetrys import ApiRetry
from typing import Dict, List, Tuple
from pyquery import PyQuery

from components import PermataComponent

class PermataLibs(PermataComponent):
    def __init__(self) -> None:
        super().__init__()

        self.api = ApiRetry(show_logs=True, defaulth_headers=True)
        ...

    def extract_bio(self, html: PyQuery) -> Tuple[str]:

        history_education = False
        term_of_office = False

        pendidikan: str | None = None
        jabatan: str | None = None
        biografi: str | None = None

        for tag in html.find('div.desc').children():

            if PyQuery(tag).is_('p') and not biografi:
                biografi = PyQuery(tag).text()
            
            if 'Riwayat Pendidikan'.lower() in PyQuery(tag).text().lower():
                history_education = True

            elif history_education:
                pendidikan = PyQuery(tag).text()
                history_education = False
                ...

            if 'Dasar Hukum & Masa Jabatan'.lower() in PyQuery(tag).text().lower():
                term_of_office = True

            elif term_of_office:
                jabatan = PyQuery(tag).text()
                term_of_office = False
                ...
            ...

        return (pendidikan, jabatan, biografi)
        ...

    def get_experience(self, html: PyQuery) -> str:
        pengalaman_kerja: List[str] = []
        ul_items = html('div.desc > ul')

        if len(ul_items) >= 1:
            for li in PyQuery(ul_items[-1]).find('li'):
                pengalaman_kerja.append(PyQuery(li).text())
            
            if len(ul_items) >= 2:
                rangkap_jabatan: List[str] = []
                for li in PyQuery(ul_items[0]).find('li'):
                    rangkap_jabatan.append(PyQuery(li).text())
            else:
                rangkap_jabatan = None
        else:
            rangkap_jabatan = None

        return ('/n'.join(pengalaman_kerja), '\n'.join(rangkap_jabatan) if rangkap_jabatan else None)
        ...

    def extract(self, html: PyQuery) -> Dict[str, str]:

        (pengalaman_kerja, rangkap_jabatan) = self.get_experience(html)
        (pendidikan, dll, biografi) = self.extract_bio(html)

        return {
            "nama_lengkap": html.find('p.name').text(),
            "nama_jabatan": html.find('p.position').text(),
            "riwayat_pendidikan": pendidikan,
            "riwayat_pekerjaan": pengalaman_kerja,
            "link_foto": self.base_url+html.find('img').attr('data-src'),
            "biografi": biografi,
            "riwayat_pencapaian": rangkap_jabatan,
            "tempat_tanggal_lahir": None,
            "organisasi": None,
            "dll": dll
            }
        ...