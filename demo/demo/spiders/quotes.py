import scrapy
from demo .items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            item = QuoteItem()
            item['text'] = quote.css('.text::text').extract_first()
            item['author'] = quote.css('.author::text').extract_first()
            item['tags'] = quote.css('.tags .tag::text').extract()
            yield item

        next = response.css('.next a::attr(href)').extract_first()  # 返回/page/2
        if next is not None:
            next_page = response.urljoin(next)  # 返回https://quotes.toscrape.com/page/2
            yield scrapy.Request(next_page, callback=self.parse)