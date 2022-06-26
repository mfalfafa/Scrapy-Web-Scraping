import scrapy

class WhiskeySpider(scrapy.Spider):
    name = 'whiskey'
    start_urls = ['https://www.thewhiskyexchange.com/c/40/single-malt-scotch-whisky']
    
    def __init__(self, *args, **kwargs):
        super(WhiskeySpider, self).__init__(*args, **kwargs)
        self.pg_count = 1
        self.next_url = 'https://www.thewhiskyexchange.com/c/40/single-malt-scotch-whisky'

    def parse(self, response):
        for products in response.css("li.product-grid__item"):
            try:
                yield {
                    "name": products.css("p.product-card__name::text").get().strip(),
                    "price": products.css("p.product-card__price::text").get().replace("£", "").strip(),
                    "link": "https://www.thewhiskyexchange.com" + products.css("a.product-card").attrib["href"],
                }
            except:
                yield {
                    "name": products.css("p.product-card__name::text").get().strip(),
                    "price": None,
                    "link": None 
                    }
        
        self.pg_count = self.pg_count + 1
        next_page = "{}?pg={}".format(self.next_url, self.pg_count)
        if self.pg_count <= 87:
            yield response.follow(next_page, callback=self.parse)

        # next_page = response.css("a.action.next").attrib["href"]
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)