import scrapy
import logging


class ActorSpider(scrapy.Spider):
    name = "actors"

    def start_requests(self):
        logging.debug("starting requests")
        urls = [
            'https://en.wikipedia.org/wiki/George_Clooney',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)