# -*- coding: utf-8 -*-
import scrapy


class BestsellersSpider(scrapy.Spider):
    name = 'BestSellers'
    allowed_domains = ['www.amazon.com']
    start_urls = ['http://www.amazon.com/']

    def start_requests(self):
        url = 'https://www.amazon.com/Best-Sellers-Home-Kitchen/zgbs/home-garden/ref=zg_bs_pg_%d?_encoding=UTF8&pg=%d&ajax=1'
        for i in range(1, 5):
            _url = url % (i, i)
            print(_url)
            yield scrapy.Request(_url, callback=self.parse)

    def parse(self, response):
        for item in response.xpath('//div[@class="zg_itemImmersion"]'):
            rank = item.xpath('//span[@class="zg_rankNumber"]/text()').extract()
            title = item.xpath('//div[@class="p13n-sc-truncate p13n-sc-line-clamp-2"]/text()').extract()
            star = item.xpath('//span[@class="a-icon-alt"]/text()').extract()
            price = item.xpath('//span[@class="p13n-sc-price"]/text()').extract()
            img = item.xpath('//img/@src').extract()
            urls = item.xpath('//a[@class="a-link-normal"]/@href').extract()
            print(rank)
            print(title)
            print(star)
            print(price)
            print(img)

            detail = []
            for index in range(len(rank)):
                if detail[index] is None:
                    detail[index] = {}
                detail[index]['rank'] = rank[index]

            for index in range(len(title)):
                if detail[index] is None:
                    detail[index] = {}
                detail[index]['title'] = title[index]

            for index in range(len(star)):
                if detail[index] is None:
                    detail[index] = {}
                detail[index]['star'] = star[index]

            for index in range(len(price)):
                if detail[index] is None:
                    detail[index] = {}
                detail[index]['price'] = price[index]

            for index in range(len(img)):
                if detail[index] is None:
                    detail[index] = {}
                detail[index]['img'] = img[index]

            for index in range(len(urls)):
                _url = 'https://www.amazon.com' + urls[index]

                yield scrapy.Request(_url, callback=self.detail_parse, meta=detail)

    def detail_parse(self, response):
        print(response.meta)
