# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.linkextractors import LinkExtractor
import redis

from heda.items import HedaItem

class HddznetSpider(scrapy.Spider):

    BASE_DOMAIN_ = 'www.hddznet.com'
    # PRODUCT_PATTERN_ = re.compile(r'product-.*.html$')
    # PROGRAM_PATTERN_ = re.compile(r'program-.*.html$')
    # NEWS_PATTERN_ = re.compile(r'news/.*.html$') 

    name = 'hddznet'
    allowed_domains = [BASE_DOMAIN_]
    start_urls = ['http://www.hddznet.com'] 

    def __init__(self):
        pool = redis.ConnectionPool(host='128.1.6.45', port=6379, decode_responses=True)
        self.redis = redis.Redis(connection_pool=pool)

    def parse(self, response):
        
        print('==>', response.url)

        title = response.xpath('//div[@class="current-menu"]/text()').extract_first()        

        item = HedaItem()
        item['title'] = title.strip() if title is not None else ''
        item['url'] = response.url
        item['company'] = 'heda'

        spans = response.xpath('//div[@class="content"]//span/text()').extract()
        ps = response.xpath('//div[@class="content"]//p/text()').extract()
        lnks = response.xpath('//div[@class="content"]//a/text()').extract()
        tds = response.xpath('//div[@class="content"]//td/text()').extract()
        item['contents'] = spans + ps + lnks + tds
        # print(spans)        

        yield item

        link_extractor = LinkExtractor(allow = r'.*')
        links = link_extractor.extract_links(response)
		
        for lnk in links:
            # URL should in base domain
            if self.BASE_DOMAIN_ not in lnk.url: 
                continue

            # match = self.PRODUCT_PATTERN_.search(lnk.url) is not None or \
            #         self.PROGRAM_PATTERN_.search(lnk.url) is not None or \
            #         self.NEWS_DETAIL_PATTERN_.search(lnk.url) is not None
                              
            # if not match: continue

            # each URL should only crawl once 
            key = 'uri:url:{0}'.format(lnk.url)
            if self.redis.exists(key): 
                continue

            yield scrapy.Request(lnk.url, callback=self.parse) 

            self.redis.set(key, lnk.url)        
    

        