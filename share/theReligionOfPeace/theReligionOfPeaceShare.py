import os
import shutil

from icecream import ic
from dotenv import load_dotenv

from library import TheReligionOfPeaceLibs
from server.kafkaa import Kafkaa
from utils import *

# Stable
class TheReligionOfPeaceShare(TheReligionOfPeaceLibs):
    def __init__(self) -> None:
        super().__init__()
        load_dotenv()

        self.kafka = Kafkaa(topic=self.topic)
        ...

    def main(self):
        (_, send) = self.read_database()

        for root, dirs, files in os.walk(self.path_stream):
            for file in files:
                file_path = os.path.join(root, file).replace('\\', '/')
                
                file: int = int(file.split('.')[0])

                if file > int(send):
                    Runtime.shareKafka(file_path)
                    data: dict = File.read_json(file_path)
                    self.kafka.send(data)
                    ...
        
        self.update_database(send_time=epoch())