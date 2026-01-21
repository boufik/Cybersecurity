import scrapy


# Author + Text
class SpiderAuthorText(scrapy.Spider):
    # Attributes
    name = "SpiderAuthorText"
    start_urls = ["https://quotes.toscrape.com/tag/humor/"]
    # Methods
    def parse(self, response):
        for quote in response.css("div.quote"):
            author = quote.xpath("span/small/text()").get()
            text = quote.css("span.text::text").get()
            item = {"author": author, "text": text}
            yield item
        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)