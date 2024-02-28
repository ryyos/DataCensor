import os

from pyquery import PyQuery
from typing import Dict, List
from icecream import ic

from ApiRetrys import ApiRetry
from server.s3 import ConnectionS3
from components import BriComponent
from utils import *


class BriLibs(BriComponent):
    def __init__(self) -> None:
        super().__init__()

        self.api = ApiRetry(show_logs=True, defaulth_headers=True)
        self.s3 = ConnectionS3(access_key_id=os.getenv('ACCESS_KEY_ID'),
                                 secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
                                 endpoint_url=os.getenv('ENDPOINT'),
                                 )
        ...

    def get_avatar(self, text: str) -> str:
        text: str = text.split('(')[-1]
        text: str = text.split(')')[0]
        return self.base_url+text
        ...

    def direksi(self, avatar: PyQuery, bio: PyQuery) -> Dict[str, any]:

        riwayat: List[PyQuery] = bio.find('div.boxRiwayatInner')

        ic(len(riwayat))
        return {
            "nama_jabatan": bio.find('div.boxName p').text(),
            "nama_lengkap": bio.find('div.boxName h3').text(),
            "riwayat_pendidikan": '\n'.join(PyQuery(li).text() for li in PyQuery(riwayat[0]).find('li')) if len(riwayat) >= 1 else None,
            "riwayat_pekerjaan": '\n'.join(PyQuery(li).text() for li in PyQuery(riwayat[1]).find('li')) if len(riwayat) >= 2 else None,
            "riwayat_pencapaian": '\n'.join(PyQuery(li).text() for li in PyQuery(riwayat[2]).find('li')) if len(riwayat) >= 3 else None,
            "link_foto": self.get_avatar(avatar.attr('style')),
            "tempat_tanggal_lahir": None,
            "biografi": None,
            "organisasi": None,
            "dll": None
        }

        ...

"""
    {
      "nama_jabatan": "CEO",
      "nama_lengkap": "John Doe",
      "riwayat_pendidikan": "S1 Informatika, Universitas ABC (2010)\nS2 Manajemen Bisnis, Universitas XYZ (2015)",
      "riwayat_pekerjaan": "Manager, Company A (2010-2015)\nDirector, Company B (2015-2020)",
      "riwayat_pencapaian": "Penghargaan Karyawan Terbaik Tahun 2012\nInovasi Terbaik Tahun 2018",
      "link_foto": "https://example.com/johndoe.jpg",
      "tempat_tanggal_lahir": "Jakarta, 15 Januari 1985",
      "biografi": "Seorang pemimpin yang berpengalaman dalam industri IT...",
      "organisasi": "Anggota Dewan Teknologi Nasional\nKetua Ikatan Manajer Bisnis",
      "dll": "Informasi tambahan lainnya"
    }

"""