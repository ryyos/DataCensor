import requests

from typing import List
from ApiRetrys import ApiRetry
from icecream import ic
from fake_useragent import FakeUserAgent

class GlassdorLibs:
    def __init__(self) -> None:

        self.api = ApiRetry(show_logs=True, defaulth_headers=False, redirect_url='https://www.glassdoor.com/')
        self.faker = FakeUserAgent()

        self.cookies = {
            'bptw-banner-closed': 'true',
            'gdId': '2e57977a-bab4-47f2-bd0e-e883e84d2534',
            '_cfuvid': 'y_CCfxtE13D6YoeMCGNPyO.c.F4bD2PNjq56j7FhGGY-1706582518564-0-604800000',
            'GSESSIONID': 'undefined',
            'JSESSIONID': '3EF64AC170789F4637ADECF549E7E27D',
            'cass': '1',
            'g_state': '{"i_p":1706589768199,"i_l":1}',
            'fpvc': '1',
            'gdsid': '1706582518154:1706582884899:0CDEF2FECEBFCB05B9A4F50D92D6674B',
            'AWSALB': '1m3HbkyQB3fd5pAPWx/8zBwvFBV4XgARWAw7z2BHGw5/tWEqeOJYOhcBTn1T/ERl/OoVh/WuHHe5Udp4Z8/K6d2dXQ3qHWkuTCFAnG35I86bLZn/T9djG8ZzKGcc',
            'AWSALBCORS': '1m3HbkyQB3fd5pAPWx/8zBwvFBV4XgARWAw7z2BHGw5/tWEqeOJYOhcBTn1T/ERl/OoVh/WuHHe5Udp4Z8/K6d2dXQ3qHWkuTCFAnG35I86bLZn/T9djG8ZzKGcc',
            'asst': '1706585022.0',
            'bs': 'E1_e_AHM_zJYW5WFOOzsuQ:rzvBvUCyIr_WK47SvyUu6CFtTjrVkBQY7Kp7LIrFERdC0mTxkgCkNiT-gOrwBG87spbxwx3llaNVvRolt5Z5r7Ju_vVfffXEcvHRLJkT4Ko:9kPMAUDtZPAX3zr2t4CHJaB_mrZm0zNDS7bDaby9vy8',
            '__cf_bm': 'A4MGkGeM.VLTV4MX54nDotW0V7FR2MprK9mk.Ym80jI-1706585027-1-AXKLfFT5GTWH5cuwoc75amDn22kpRsK3EYQyfR3EkA/4fjxXgfHvtFZMsAK1b66lP4KBgNkm14DX4T+NEaOwK2kKDnbEI+YJpTxKDDiMKo4U',
        }

        self.headers = {
            'authority': 'www.glassdoor.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9,id;q=0.8',
            'cache-control': 'max-age=0',
            # 'cookie': 'bptw-banner-closed=true; gdId=2e57977a-bab4-47f2-bd0e-e883e84d2534; _cfuvid=y_CCfxtE13D6YoeMCGNPyO.c.F4bD2PNjq56j7FhGGY-1706582518564-0-604800000; GSESSIONID=undefined; JSESSIONID=3EF64AC170789F4637ADECF549E7E27D; cass=1; g_state={"i_p":1706589768199,"i_l":1}; fpvc=1; gdsid=1706582518154:1706582884899:0CDEF2FECEBFCB05B9A4F50D92D6674B; AWSALB=1m3HbkyQB3fd5pAPWx/8zBwvFBV4XgARWAw7z2BHGw5/tWEqeOJYOhcBTn1T/ERl/OoVh/WuHHe5Udp4Z8/K6d2dXQ3qHWkuTCFAnG35I86bLZn/T9djG8ZzKGcc; AWSALBCORS=1m3HbkyQB3fd5pAPWx/8zBwvFBV4XgARWAw7z2BHGw5/tWEqeOJYOhcBTn1T/ERl/OoVh/WuHHe5Udp4Z8/K6d2dXQ3qHWkuTCFAnG35I86bLZn/T9djG8ZzKGcc; asst=1706585022.0; bs=E1_e_AHM_zJYW5WFOOzsuQ:rzvBvUCyIr_WK47SvyUu6CFtTjrVkBQY7Kp7LIrFERdC0mTxkgCkNiT-gOrwBG87spbxwx3llaNVvRolt5Z5r7Ju_vVfffXEcvHRLJkT4Ko:9kPMAUDtZPAX3zr2t4CHJaB_mrZm0zNDS7bDaby9vy8; __cf_bm=A4MGkGeM.VLTV4MX54nDotW0V7FR2MprK9mk.Ym80jI-1706585027-1-AXKLfFT5GTWH5cuwoc75amDn22kpRsK3EYQyfR3EkA/4fjxXgfHvtFZMsAK1b66lP4KBgNkm14DX4T+NEaOwK2kKDnbEI+YJpTxKDDiMKo4U',
            'referer': 'https://www.glassdoor.com/',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        ...

    def collect_companies(self, url: str) -> List[str]:
        response = requests.get(url=url, headers=self.headers, cookies=self.cookies)
        ic(response)
        ic(response.text)
        ...