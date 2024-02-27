import requests

from pyquery import PyQuery
from icecream import ic

cookies = {
    'donation-identifier': 'fe177952f6e4f1e7c531e98e051f07cb',
    'abtest-identifier': '1c812059527dcb706ca3b624470a2f99',
    'view-search': 'tiles',
    'showdetails-search': '',
}

headers = {
    'authority': 'archive.org',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,id;q=0.8',
    # 'cookie': 'donation-identifier=fe177952f6e4f1e7c531e98e051f07cb; abtest-identifier=1c812059527dcb706ca3b624470a2f99; view-search=tiles; showdetails-search=',
    'referer': 'https://archive.org/details/iraq_middleeast?page=2',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
}

params = {
    'user_query': '',
    'page_type': 'collection_details',
    'page_target': 'iraq_middleeast',
    'hits_per_page': '50',
    'page': '201',
    'aggregations': 'false',
    'uid': 'R:4a274dd0e63e6ba9ee25-S:624d48557de92430fec8-P:3-K:h-T:1708944506957',
    'client_url': 'https://archive.org/details/iraq_middleeast?page=200',
}

