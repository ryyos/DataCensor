import requests

class Down:

    @staticmethod
    def curl(url: str, path: str, headers: dict = None, cookies: dict = None) -> None:
        image = requests.get(url=url, headers=headers, cookies=cookies)
        with open(path, 'wb') as f:
            f.write(image.content)
