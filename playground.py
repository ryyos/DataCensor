import requests
from typing import List
from pyquery import PyQuery
from icecream import ic



def get_url(url, headers):
    response = requests.get(url, headers=headers)
    html = PyQuery(response.text)

    urls = []

    for a in html.find('div[class="sc-3450242-3 fLFQmt ipc-page-grid__item ipc-page-grid__item--span-2"] ul li a'):
        urls.append(PyQuery(a).attr('href'))

    return urls

def extract(web_url, headers):
    response = requests.get(web_url, headers=headers)
    html = PyQuery(response.text)

    results = {
        "Title": html.find('div[class="sc-69e49b85-0 jqlHBQ"] h1').text(),
        "Rating": html.find('div[class="sc-bde20123-2 cdQqzc"] span[class="sc-bde20123-1 cMEQkK"]').text().split(' ')[0],
        "Year": html.find('li[data-testid="title-details-releasedate"] div ul li a').text().split(" ")[-2],
        "Month": html.find('li[data-testid="title-details-releasedate"] div ul li a').text().split(' ')[0]
    }

    ic(results)
    (month, date, year, country) = html.find('li[data-testid="title-details-releasedate"] div ul li a').text().split(" ")
    # print(results)

def execute():
    base_url = 'https://m.imdb.com'
    main_url = 'https://m.imdb.com/chart/top/?ref_=nv_mv_250'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
    }

    page = 1
    while True:
        urls = get_url(main_url, headers)
        for url in urls:
            extract(base_url+url, headers)
            break
        break
        
            


execute()