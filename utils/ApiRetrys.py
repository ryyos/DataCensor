import requests

from time import sleep
from .runtime import logger
from icecream import ic
from fake_useragent import FakeUserAgent
from requests import Session

class ApiRetry:

    def __init__(self) -> None:
        self.__faker = FakeUserAgent(browsers='chrome', os='windows')
        self.__sessions = Session()

        self.RESPONSE_CODE = [200, 400, 404, 500]
    
    def retry(self, url: str, 
                action: str, 
                payload: dict = None, 
                retry_interval: int = 1,
                refresh: str = None
                ):


        match action:

            case 'get':
                retry = 0
                while True:
                    try:
                        response = self.__sessions.get(url=url, headers={'User-Agent': self.__faker.random})


                        logger.info(f'user agent: {self.__faker.random}')
                        logger.info(f'response status: {response.status_code}')
                        logger.info(f'try request in url: {url}')
                        logger.info(f'request action: {action}')
                        print()

                        if response.status_code in self.RESPONSE_CODE: return response
                        if response.status_code == 403:
                            ic(response.text)
                            self.__sessions.get(url=refresh, headers={'User-Agent': self.__faker.random})


                        sleep(retry_interval)

                        logger.warning(f'response status: {response}')
                        logger.warning(f'retry interval: {retry_interval}')
                        logger.warning(f'retry to: {retry}')
                        print()

                        retry_interval+=5
                        retry+=1

                    except Exception as err:

                        logger.error(err)
                        logger.warning(f'retry interval: {retry_interval}')
                        logger.warning(f'retry to: {retry}')
                        print()

                        sleep(retry_interval)
                        retry_interval+=5

                return response


            case 'post':

                retry = 0
                for _ in range(5):
                    try:
                        
                        response = self.__sessions.post(url=url, json=payload, headers={
                                "User-Agent": self.__faker.random,
                                "Content-Type": "application/json"
                            })

                        logger.info(f'response status: {response.status_code}')
                        logger.info(f'try request in url: {url}')
                        logger.info(f'request action: {action}')
                        print()

                        if response.status_code in self.RESPONSE_CODE: return response
                        if response.status_code == 403: 
                            ic(response.text)
                            self.__sessions.get(url=refresh, headers={"User-Agent": self.__faker.random})

                        logger.warning(f'retry interval: {retry_interval}')
                        logger.warning(f'retry to: {retry}')
                        logger.warning(f'response status: {response}')
                        
                        sleep(retry_interval)
                        retry_interval+=5
                    except Exception as err:
                        logger.error(err)
                        logger.warning(f'retry interval: {retry_interval}')
                        logger.warning(f'response status: {response}')
                        logger.warning(f'retry to: {retry}')
                        retry+=1

                        sleep(retry_interval)
                        retry_interval+=5

            