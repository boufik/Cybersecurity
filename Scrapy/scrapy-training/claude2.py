import scrapy


# AdvancedSpider
class AdvancedSpider(scrapy.Spider):
    # Attributes
    name = "AdvancedSpider"
    start_urls = ["https://quotes.toscrape.com/"]
    custom_settings = {'DOWNLOAD_DELAY': 1, 'USER_AGENT': 'Mozilla/5.0 (compatible; QuotesBot/1.0)'}
    # Methods
    def parse(self, response):
        for quote in response.css('div.quote'):
            tags = quote.css('div.tags a.tag::text').getall()
            # Only yield quotes tagged with 'life' or 'inspirational'
            if any(tag in ['life', 'inspirational'] for tag in tags):
                author = quote.css('small.author::text').get()
                item = {'author': author, 'tags': tags}
                yield item
        # Follow pagination links <a> to next pages
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
