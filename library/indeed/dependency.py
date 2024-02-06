import asyncio

from ApiRetrys import ApiRetry
from icecream import ic
from time import sleep
from pyquery import PyQuery
from browser import Playwright
from playwright.sync_api import Page, Response
from typing import List

class IndeedLibs:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.api = ApiRetry(show_logs=True)

        self.MAIN_URL = 'https://id.indeed.com'
        self.DOMAIN = 'id.indeed.com'
        self.LINK = 'https://id.indeed.com/companies'

        ...

    async def get_companies(self, page: Page) ->List[str]:
        await page.goto(self.LINK)

        return await page.eval_on_selector_all('div[data-tn-element="CompanyUrlLink"] a', '(as) => as.map(a => a.href)')
        ...
