
from typing import Dict

from library import DownloadLibs
from utils import *

class Download(DownloadLibs):
    def __init__(self, save: bool, s3: bool) -> None:
        super().__init__()

        self.SAVE_TO_LOCAL = save,
        self.SAVE_TO_S3 = s3
        ...

    def metadata(self, url: str, domain: str) -> Dict[str, any]:

        headers = {
            "link": url,
            "domain": domain,
            "tags": [domain],
            "crawling_time": now(),
            "crawling_time_epoch": epoch(),
            "path_data_raw": "",
            "path_data_clean": "",
            "path_data_document": "",
            "title": self.get_title(url)
        }
        ...

    def main(self, url: str, domain: str) -> None:
        headers = self.metadata(url, domain)

        if self.SAVE_TO_LOCAL:
            Down.curl()
        ...