import scrapy


# Author
class SpiderAuthor(scrapy.Spider):
    # Attributes
    name = "SpiderAuthor"
    start_urls = ["https://quotes.toscrape.com/tag/humor/"]
    # Methods
    def parse(self, response):
        for quote in response.css("div.quote"):
            author = quote.xpath("span/small/text()").get()
            item = {"author": author}
            yield item
        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)