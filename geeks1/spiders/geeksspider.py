import scrapy
import requests

class GeeksSpider(scrapy.Spider):
    name = "geeks"
    start_url = 'http://www.geeksforgeeks.org/category/linked-list/page/'
    global filename

    def start_requests(self):
        topics = ['linked-list', 'c-arrays']
        for topic in topics :
            i=1
            start_url = 'http://www.geeksforgeeks.org/category/'+topic+'/page/'
            filename = topic + '.html'
            test = requests.get(start_url+str(i))
            while(str(test.status_code) == '200') :
                yield scrapy.Request(url=start_url+str(i), callback = self.nest)
                i+=1
                test = requests.get(start_url+str(i))
                print 'i         ==================              ' + str(i)


    def parse(self, response):
        self.log('Reached')
        content = response.css('div.entry-content').extract_first().encode('utf-8')
        filtered_content = Selector(text=content).xpath('//*[not(self::h1)]').extract_first().encode('utf-8')
        with open(filename, 'a') as f:
            f.write(filtered_content)

    def nest(self, response):
        self.log(response.css('header.entry-header a::attr(href)').extract_first())
        for page in response.css('header.entry-header a::attr(href)').extract():
            self.log(page)
            yield scrapy.Request(url=page, callback = self.parse)