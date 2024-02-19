import os
import shutil

from icecream import ic

from dotenv import load_dotenv
from server.kafkaa import Kafkaa
from utils import Runtime, File

class ShareKafka:
    def __init__(self, base_path: str, topic: str) -> None:
        load_dotenv()

        self.base_path = base_path
        self.kafka = Kafkaa(topic=topic)
        ...

    def main(self):

        for root, dirs, files in os.walk(self.base_path):
            for file in files:

                if file.endswith('json'):
                    file_path = os.path.join(root, file).replace('\\', '/')
                    
                    Runtime.shareKafka(file_path)

                    data: dict = File.read_json(file_path)
                    self.kafka.send(data)
