import asyncio

from icecream import ic
from playwright.sync_api import sync_playwright, BrowserContext, Browser
from time import sleep

class SyncPlaywright:
    def __init__(self) -> None:
        ...

    @staticmethod
    def browser() -> BrowserContext:
        playwright = sync_playwright().start()
        browser: Browser = playwright.chromium.launch(headless=False, args=['--window-position=-8,-2'])
        browser: BrowserContext = browser.new_context()
        return browser
    

if __name__== '__main__':
    bro = Browser()
    bro.browser()