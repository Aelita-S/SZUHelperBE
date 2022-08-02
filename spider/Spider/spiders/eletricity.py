import scrapy


class EletricitySpider(scrapy.Spider):
    name = 'eletricity'
    start_urls = ['http://192.168.84.3:9090/']

    def parse(self, response):
        pass
