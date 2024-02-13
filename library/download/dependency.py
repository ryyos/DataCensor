import urllib.parse

class DownloadLibs:
    def __init__(self) -> None:
        ...

    def get_title(self, url: str) -> str:
        decoded = urllib.parse.unquote(url.replace('+', ' '))
        return decoded.split('/')[-1]
        ...