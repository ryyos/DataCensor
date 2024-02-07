import requests
from urllib import request

from icecream import ic

url = 'https://dc601.4shared.com/download/1VEFZFf8/Islam_Denounces_Terrorism.pdf?tsid=20240207-101049-91cebb6b&sbsr=dd1c29d0ab4bea62707bb7234db51aacb06&bip=MTgyLjIuMTQ1LjA&lgfp=30'


cookies = {
    'day1host': 'h',
    'hostid': '-528958367',
    'dlpvc110439': 'N',
    'cd1v': 'A-bak9baPlT5',
    'Login': '1531194522',
    'Password': '8a85738e0f6d41d3632e4f86a9c08c4e',
    'ulin': 'true',
    '4langcookie': 'in',
    'JSESSIONID': 'BB3D9F8AAF7CD63065DD9037BBE59AEB.dc571',
    'WWW_JSESSIONID': 'BB3D9F8AAF7CD63065DD9037BBE59AEB.dc571',
    'showApkOwnerGuidenJ2RwU2o': 'null',
    'utrf': '9f5d09323c',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
    'Connection': 'keep-alive',
    # 'Cookie': 'day1host=h; hostid=-528958367; dlpvc110439=N; cd1v=A-bak9baPlT5; Login=1531194522; Password=8a85738e0f6d41d3632e4f86a9c08c4e; ulin=true; 4langcookie=in; JSESSIONID=BB3D9F8AAF7CD63065DD9037BBE59AEB.dc571; WWW_JSESSIONID=BB3D9F8AAF7CD63065DD9037BBE59AEB.dc571; showApkOwnerGuidenJ2RwU2o=null; utrf=9f5d09323c',
    'Referer': 'https://www.4shared.com/get/1VEFZFf8/Islam_Denounces_Terrorism.html',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'locale': 'in',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'x-security': '1531194522',
}


def curl(url: str, path: str):

    image = requests.get(url=url, headers=headers, cookies=cookies)
    ic(image)
    with open(path, 'wb') as f:
        f.write(image.content)

curl(url, 'private/44.pdf')

class FourShared:
    def __init__(self) -> None:
        pass