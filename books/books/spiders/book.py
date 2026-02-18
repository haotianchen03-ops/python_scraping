import scrapy
from scrapy_playwright.page import PageMethod

class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["spa5.scrape.center"]
    start_url = "https://spa5.scrape.center/page/{page}"
    max_page = 10

    def start_requests(self):
        for page in range(1,self.max_page+1):
            url = self.start_url.format(page = page)
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,  # 开启 Playwright 渲染
                    "playwright_context_kwargs": {
                        "ignore_https_errors": True,  # ⭐ 关键
                    },
                    "playwright_page_methods": [
                        PageMethod("wait_for_load_state", "networkidle"),  # 等待网络请求完成
                    ],
                },
            )

    def parse(self, response):
        for book in response.css('.item'):
            name = book.css('.name::text').extract_first()
            authors = book.css('.author::text').extract_first()
            name = name.strip() if name else None
            authors = authors.strip() if authors else None
            yield {
                'name': name,
                'authors': authors
            }

