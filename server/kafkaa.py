import os
import json

from dotenv import load_dotenv
from kafka import KafkaProducer

class Kafkaa:
    load_dotenv()
    def __init__(self, topic: str) -> None:

        self.__kafka_produser = KafkaProducer(bootstrap_servers=[os.getenv('KAFKA01'), os.getenv('KAFKA02'), os.getenv('KAFKA03')])
        self.__topic: str = topic
        ...

    def send(self, data: dict) -> None:
        self.__kafka_produser.send(topic=self.__topic, value=str.encode(json.dumps(data)))


   
