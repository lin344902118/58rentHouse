# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from rentHousse.items import RenthousseItem

MIN_RENT = 1000
MAX_RENT = 1500
MAX_PAGE = 2

class rent58Spider(Spider):
    name = "rent58"
    allowed_domains = ["58.com"]
    start_urls = []

    def start_requests(self):
        url = 'http://xm.58.com/pinpaigongyu/pn/{page}/minprice={min_rent}_{max_rent}'

        for i in range(1, MAX_PAGE):
            if i == 1:
                url = 'http://xm.58.com/pinpaigongyu/?minprice=1000_1500'
            else:
                url = url.format(page=i, min_rent=MIN_RENT, max_rent=MAX_RENT)
            print url
            self.start_urls.append(url)

        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        response = response.replace(body=response.body.replace('<b>', ''))
        hxs = Selector(response)
        contents = hxs.xpath('//ul[@class="list"]/li')
        item = RenthousseItem()
        for i in range(len(contents)):
            item['title'] = contents[i].xpath('//*[@class="des"]/h2/text()')[i].extract().replace(' ', '').decode()
            item['condition'] = contents[i].xpath('//*[@class="des"]/p[@class="room"]/text()')[i].extract().replace(' ', '').replace('\r\n', '').decode()
            try:
                item['remarks'] = contents[i].xpath('//*[@class="des"]/p[@class="spec"]/span[@class="spec1"]/text()')[i].extract().replace(' ', '').decode()
            except:
                item['remarks'] = ''
            item['price'] = contents[i].xpath('//*[@class="money"]/span/text()')[i].extract().replace(' ', '').replace('\r\n', '').decode()
            yield item
