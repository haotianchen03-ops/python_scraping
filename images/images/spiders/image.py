import scrapy
from scrapy import Request, Spider
import json
from images.items import ImagesItem


class ImageSpider(scrapy.Spider):
    name = "image"
    allowed_domains = ["baidu.com"]
    start_urls = ["https://image.baidu.com"]

    def parse(self, response):
        try:
            result = json.loads(response.text)
        except json.JSONDecodeError:
            self.logger.error("JSON 解析失败: %s", response.text[:200])
            return

        inspiration = result.get("inspiration") or {}
        inspirations = inspiration.get("inspirations") or []

        for image in inspirations:
            item = ImagesItem()
            item["description"] = image.get("description")
            labels = image.get("labels", [])
            item["labels"] = labels[0].get("label") if labels else ""
            item["url"] = image.get("img")
            yield item

    def start_requests(self):
        base_url = "https://image.baidu.com/aigc/inspirepics?"
        rn = 20
        for page in range(1,self.settings.get('MAX_PAGE')+1):
            pn = page*rn
            url = f'{base_url}&pn={pn}&rn={rn}'
            yield scrapy.Request(url, callback=self.parse)
