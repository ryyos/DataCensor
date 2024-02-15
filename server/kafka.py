import json

from kafka import KafkaProducer

class Kafka:
    def __init__(self, topic: str, server: str) -> None:

        self.__kafka_produser = KafkaProducer(bootstrap_servers=server)
        self.__topic: str = topic
        ...

    def send(self, data: dict) -> None:
        self.__kafka_produser.send(topic=self.__topic, value=bytes(json.dumps(data.json()), 'utf-8'))