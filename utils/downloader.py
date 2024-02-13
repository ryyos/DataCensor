import requests

from requests import Response
class Down:

    @staticmethod
    def curl(url: str, path: str, headers: dict = None, cookies: dict = None) -> Response:
        response = requests.get(url=url, headers=headers, cookies=cookies)
        with open(path, 'wb') as f:
            f.write(response.content)

        return response
    
    @staticmethod
    def curlv2(path: str, response: Response) -> Response:
        with open(path, 'wb') as f:
            f.write(response.content)

    
