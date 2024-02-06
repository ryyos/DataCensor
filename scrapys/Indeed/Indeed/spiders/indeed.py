import scrapy


class IndeedSpider(scrapy.Spider):
    name = "indeed"
    allowed_domains = ["id.indeed.com"]
    start_urls = ["https://id.indeed.com"]

    def parse(self, response):
        pass
