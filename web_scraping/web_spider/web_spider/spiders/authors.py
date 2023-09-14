import scrapy


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "authors.json"}

    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            author_link = quote.xpath("span/a/@href").get()
            yield response.follow(author_link, self.author_parse)

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def author_parse(self, response):
        fullname = response.xpath("//h3[@class='author-title']/text()").get()
        born_date = response.xpath("//span[@class='author-born-date']/text()").get()
        born_location = response.xpath(
            "//span[@class='author-born-location']/text()"
        ).get()
        description = response.xpath("//div[@class='author-description']/text()").get()

        yield {
            "fullname": fullname,
            "born_date": born_date,
            "born_location": born_location,
            "description": description,
        }
