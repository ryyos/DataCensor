import asyncio

from icecream import ic
from playwright.async_api import async_playwright, BrowserContext, Browser
from time import sleep

class Playwright:
    def __init__(self) -> None:
        ...

    @staticmethod
    async def browser() -> BrowserContext:
        playwright =await async_playwright().start()
        browser: Browser = await playwright.chromium.launch(headless=False, args=['--window-position=-8,-2'])
        browser: BrowserContext = await browser.new_context()
        return browser
    

if __name__== '__main__':
    bro = Browser()
    bro.browser()