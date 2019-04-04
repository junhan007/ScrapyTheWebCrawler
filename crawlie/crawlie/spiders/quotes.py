import scrapy 
from scrapy.loader import ItemLoader
from crawlie.items import CrawlieItem

class QuotesScraper(scrapy.Spider):
    name = "quotes"
    
    def start_requests(self):
        start_urls = [
            'https://docs.spring.io/spring/docs/'
           
        ]
        for url in start_urls: 
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self,response):
        urls = response.xpath("//a[contains(@href,'1.1.2')]//@href").extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.download)

    def  download(self,response):
           # page = response.url.split("/")[-2]
            for link in response.xpath("//a[contains(@href,'changelog')]"):
                loader = ItemLoader(item=CrawlieItem(), selector = link)
                relative_url = link.xpath(".//@href").extract_first()
                absolute_url = response.urljoin(relative_url)
                loader.add_value('file_urls', absolute_url)
                yield loader.load_item()
         
            # filename = 'quotes-%s.txt' % page
            # with open(filename, 'a') as f:
            #     f.write(str(item))
            # yield item
            # self.log('Saved file %s' % filename)



        

    