
from requests import Response
from icecream import ic

from library import JihadimalmoLibs

class Jihadimalmo(JihadimalmoLibs):
    def __init__(self, s3: bool, save: bool, thread: bool) -> None:
        super().__init__()

        self.SAVE_TO_S3 = s3
        self.SAVE_TO_LOKAL = save
        self.USING_THREADS = thread
        ...

    def main(self) -> None:
        response: Response = self.api.get(self.main_url)

        ...