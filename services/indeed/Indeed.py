import asyncio

from time import time
from library import IndeedLibs
from pyquery import PyQuery
from icecream import ic
from playwright.async_api import Page
from browser import Playwright
from utils import *

class Indeed(IndeedLibs):
    def __init__(self) -> None:
        super().__init__(self)
        asyncio.get_event_loop().run_until_complete(self.main())

    async def extract_company(self, url: str, page: Page) -> None:
        await page.goto(url)
        html = PyQuery(str(page.content))

        headers = {
        "link": self.LINK,
        "domain": self.DOMAIN,
        "tag": [self.DOMAIN],
        "crawling_time": now(),
        "crawling_time_epoch": int(time()),
        "path_data_raw": "",
        "path_data_clean": "",
        "reviews_name": html.find('div[itemprop="name"]').text(),
        "location_reviews": None,
        "category_reviews": "kerja",
        
        "salaries": [{
            "salary": PyQuery(salary).find('span.cmp-SalaryCategoryCard-title').text(),
            "value": PyQuery(salary).find('span.cmp-SalaryCategoryCard-SalaryValue').text(),
            "count": PyQuery(salary).find('span.cmp-SalaryCategoryCard-SalaryCount').text(),
        } for salary in html.find()],

        "total_reviews": html.find('div[class="css-104u4ae eu4oa1w0"]').text(),
        "reviews_rating": {
            "total_rating": "integer",
            "detail_total_rating": [
                {
                    "score_rating": "integer",
                    "category_rating": "string"
                }
            ]
        }
     }
        
        ic(headers)
        ...

    async def main(self) -> None:
        browser = await Playwright.browser()
        page = await browser.new_page()

        companies = await self.get_companies(page)
        for company in companies:
            await self.extract_company(company, page)
            break

        await page.close()
        await browser.close()
        ...
