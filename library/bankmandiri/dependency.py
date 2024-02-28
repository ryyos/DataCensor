import os

from ApiRetrys import ApiRetry
from pyquery import PyQuery
from typing import Dict, List
from server.s3 import ConnectionS3
from dotenv import load_dotenv
from icecream import ic

from components import BankmandiriComponent
from utils import *

class BankmandiriLibs(BankmandiriComponent):
    def __init__(self) -> None:
        super().__init__()
        load_dotenv()

        self.api = ApiRetry(show_logs=True)
        self.s3 = ConnectionS3(access_key_id=os.getenv('ACCESS_KEY_ID'),
                                 secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
                                 endpoint_url=os.getenv('ENDPOINT'),
                                 )
        ...

    def extract_bio(self, profile: PyQuery, index: int) -> str:
        bio: PyQuery = profile.find('div[class="detailProfile"]')
        bio: str = '\n\n'.join([PyQuery(p).text() for p in PyQuery(bio.find('p'))]) if len(profile.find('p')) > 1 else PyQuery(profile.find('p')).text()

        try:
            texts: List[str] = bio.split('\n\n')

            text: str = texts[index]
            text: str = text.split(':')[-1].strip()
            return text if not text.startswith('- ') else text[2:]
        
        except Exception as err: 
            print(err)
            return None
        ...

    def extract(self, html: PyQuery) -> Dict[str, str]:

        profile: PyQuery = html.find('div[class="org-profile-desc"]')
        return {
            "nama_jabatan": PyQuery(profile.find('p')[0]).text(),
            "nama_lengkap": profile.find('h4').text(),
            "riwayat_pendidikan": self.extract_bio(profile, 1),
            "riwayat_pekerjaan": self.extract_bio(profile, 2),
            "riwayat_pencapaian": None,
            "link_foto": self.base_url+profile.find('img').attr('src'),
            "tempat_tanggal_lahir": self.extract_bio(profile, 0),
            "biografi": None,
            "organisasi": None,
            "dll": None
            }
        ...
