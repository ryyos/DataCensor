
from requests import Response
from typing import Dict, List, Tuple
from ApiRetrys import ApiRetry
from pyquery import PyQuery
from icecream import ic

from components import BcaComponent

class BcaLibs(BcaComponent):
    def __init__(self) -> None:
        super().__init__()

        self.api = ApiRetry(show_logs=True, defaulth_headers=True)
        ...

    def extract_bio(self, html: PyQuery, type: str) -> Tuple[str]:

        main_data = html.find('div[class="col-md-8"]')

        h3_find: bool = False
        results: List[str] = []

        jabatan: str = main_data.find('h2').text() if main_data.find('h2') else PyQuery(main_data.find('p')[0]).text()
        nama: str = PyQuery(main_data.find('p')[0]).text() if main_data.find('h2') else PyQuery(main_data.find('p')[1]).text()

        childs: List[any] = main_data.children()

        if len(childs) <= 1:
            main_data = html.find('div[class="col-md-8"] > div')
            childs = main_data.children()

        temp: List[str] = []
        for index, child in enumerate(childs):

            if PyQuery(child).is_('h3'):
                results.append('\n'.join(temp))
                h3_find = True
                temp.clear()

            elif PyQuery(child).is_('p') and h3_find:
                if PyQuery(child).text(): temp.append(PyQuery(child).text())

                try:
                    if PyQuery(childs[index+1]).is_('h3'):
                        h3_find = False

                except Exception:
                    results.append('\n'.join(temp))
                    break

        
        results = [item for item in results if item.strip() != '']

        ic(len(results))

        try:
            bio: str = results[0]
            pengalaman_kerja: str = results[2] if 'direksi' == type else results[1]
            pendidikan: str = results[3] if 'direksi' == type else results[2]
            organisasi: str = results[4] if 'direksi' == type else results[3]
            pencapaian: str = results[5] if 'direksi' == type else results[4]
            dll: str = results[5]

        except Exception:
            ...

        temp.clear()
        if len(results) <= 1:
            results.clear()
            for div in html.find('div[class="col-md-8"] div[class="a-text a-text-subtitle mt-32"]'):

                childs = PyQuery(div).children()
                for index, p in enumerate(childs):
                    
                    if PyQuery(p).is_('p'):
                        temp.append(PyQuery(p).text())

                        if index+1 == len(childs):
                            results.append('\n'.join(temp))
                    elif PyQuery(p).is_('h3'):
                        results.append('\n'.join(temp))
                        temp.clear()

            ic(len(results))
            bio: str = PyQuery(html.find('p[class="a-text a-text-body a-text-brownish-grey"]')[0]).text()
            pengalaman_kerja: str = results[1]
            pendidikan: str = results[2]
            organisasi: str = results[3]
            pencapaian: str = results[4]
            dll: str = results[5]

        results = [item for item in results if len(item.strip()) > 5]

        return (nama, jabatan, bio, pengalaman_kerja, pendidikan, organisasi, pencapaian, dll)
        
        ...

    def extract(self, url: str = 'https://www.bca.co.id/id/tentang-bca/korporasi/Manajemen-BCA/profile?p={711BD376-7CE0-4B09-A019-B1FCA5E7328A}', type: str = 'direksi') -> Dict[str, str]:
        response: Response = self.api.get(url)
        html = PyQuery(response.text)
        
        (nama, 
         jabatan, 
         bio, 
         pengalaman_kerja, 
         pendidikan, 
         organisasi, 
         pencapaian, 
         dll) = self.extract_bio(html, type)

        return {
            "nama_lengkap": nama,
            "nama_jabatan": jabatan,
            "riwayat_pendidikan": pendidikan,
            "riwayat_pekerjaan": pengalaman_kerja,
            "link_foto": self.base_url+html.find('div[class="a-card-img shine"] img').attr('src'),
            "biografi": bio,
            "riwayat_pencapaian": pencapaian,
            "organisasi": organisasi,
            "dll": dll,
            "tempat_tanggal_lahir": None,
            }
        ...