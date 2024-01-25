from pyquery import PyQuery

def __fetch_categories(self, url: str) -> List[str]:
    response: Response = self.__retry(url=url)
    html = PyQuery(response.text)

    ic(url)

    categories_urls = [PyQuery(categories).attr('href') for categories in html.find('#sidenav-menu a[class="menu-categories__link"]')]
    
    return categories_urls