import scrapy


# Simple Spider
class SimpleSpider(scrapy.Spider):
    # Attributes
    name = "SimpleSpider"
    start_urls = ["https://quotes.toscrape.com/page/1/"]
    # Methods
    def parse(self, response):
        for quote in response.css('div.quote'):
            author = quote.css('small.author::text').get()
            tags = quote.css('div.tags a.tag::text').getall()
            item = {'author': author, 'tags': tags}
            yield item 
        # Follow pagination links <a> to next pages
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
