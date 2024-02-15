import os
import shutil

from icecream import ic

from dotenv import load_dotenv
from server.kafka import Kafka
from utils import *

class ShareKafka:
    def __init__(self, base_path: str, topic: str, server: str) -> None:
        load_dotenv()

        self.base_path = base_path
        self.kafka = Kafka(topic=topic, server=server)
        ...

    def main(self):
        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                file_path = os.path.join(root, file).replace('\\', '/')
                
                Runtime.share(file_path)

                data: dict = File.read_json(file_path)
                self.kafka.send(data)