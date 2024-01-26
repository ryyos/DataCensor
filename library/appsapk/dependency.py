

from typing import List
from pyquery import PyQuery

from utils import *

class AppsApkLibs:
    def __init__(self) -> None:
        ...

    def collect_apps(self, url_page: str) -> List[str]:
        response = self.__retry(url_page)
        html = PyQuery(response.text)

        apps = html.find('article.vce-post.post.type-post.status-publish.format-standard.has-post-thumbnail.hentry h2 a')

        return apps
            