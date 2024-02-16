import os
import shutil

from icecream import ic
from dotenv import load_dotenv

from library import TheReligionOfPeaceLibs
from server.kafka import Kafka
from utils import *

class TheReligionOfPeaceShare(TheReligionOfPeaceLibs):
    def __init__(self, base_path: str, topic: str, server: str) -> None:
        super().__init__()
        load_dotenv()

        self.base_path = base_path
        # self.kafka = Kafka(topic=topic, server=server)
        ...

    def main(self):
        (_, send) = self.read_database()

        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                file_path = os.path.join(root, file).replace('\\', '/')
                
                file: int = int(file.split('.')[0])
                Runtime.share(file_path)

                if file > int(send):
                    data: dict = File.read_json(file_path)
                    # self.kafka.send(data)
                    ic(file)
                    ...
        
        self.update_database(send_time=epoch())