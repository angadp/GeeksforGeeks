import scrapy
import pdfkit
import requests

class GeeksSpider(scrapy.Spider):
    name = "geeks"
    start_url = 'http://www.geeksforgeeks.org/category/linked-list/page/'

    def start_requests(self):
        i=1
        start_url = 'http://www.geeksforgeeks.org/category/linked-list/page/'
        test = requests.get(start_url+str(i))
        yield scrapy.Request(url=start_url+str(i), callback = self.nest)


    def parse(self, response):
        self.log('Reached')
        filename = 'geeks.html'
        content1 = response.css('div.entry-content').extract_first().encode('utf-8')
        with open(filename, 'a') as f:
            f.write(content1)

    def nest(self, response):
        self.log(response.css('header.entry-header a::attr(href)').extract_first())
        for page in response.css('header.entry-header a::attr(href)').extract():
            self.log(page)
            yield scrapy.Request(url=page, callback = self.parse)