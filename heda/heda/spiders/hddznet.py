# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import redis

from heda.items import ContentItem
from utils.text_helper import clear_content

class HddznetSpider(CrawlSpider):

    __BASE_DOMAIN = 'www.hddznet.com'

    name = 'hddznet'
    allowed_domains = [ __BASE_DOMAIN ]
    start_urls = ['http://www.hddznet.com'] 
    rules = (        

        # 提取 产品中心
        Rule(LinkExtractor(allow=(r'product-.*.html$')), follow=True, callback='parse_product'),

        # 提取 方案与案例
        Rule(LinkExtractor(allow=(r'program-.*.html$')), follow=True, callback='parse_program'),        

        # 提取 经典案例
        Rule(LinkExtractor(allow=(r'news/detail.*-jdal.html$')), follow=True, callback='parse_case'),

        # 提取 新闻中心
        Rule(LinkExtractor(allow=(r'news/detail.*-xwzx.html$')), follow=True, callback='parse_news'),

        # # 提取 图片 .png .jpg .jpeg .bmp
        # Rule(LinkExtractor(allow=(r'www.hddznet.com'), deny_extensions=set(), tags=('img'), attrs=('src'), canonicalize=True, unique=True), \
        #     follow=False, callback='parse_images')

        # 提取 所有链接
        Rule(LinkExtractor(allow=(r'.*')), follow=True),        
    )

    def __init__(self, *args, **kwargs):
        super(HddznetSpider, self).__init__(*args, **kwargs)
        pool = redis.ConnectionPool(host='128.1.6.45', port=6379, decode_responses=True)
        self.redis = redis.Redis(connection_pool=pool) 

    def __parse(self, response, parse_name, title_class, content_class):
        cache_key = 'uri:url:{0}'.format(response.url)
        if self.redis.exists(cache_key):
            print('xx> SKIP', self.name, response.url, parse_name)
            return None

        title = self.__extract_title(response, '//div[@class="{0}"]/text()'.format(title_class))
        print('==>', self.name, response.url, parse_name, title)
                
        elements = response.xpath('//div[@class="{0}"]//span|//div[@class="{0}"]//p|//div[@class="{0}"]//td'.format(content_class))
        contents = elements.xpath('text()').extract()
        content = clear_content(contents)
        
        item = ContentItem()
        item['company'] = self.name
        item['title'] = title
        item['url'] = response.url
        item['content'] = content

        return item
 
    def parse_product(self, response):
        yield self.__parse(response, '产品中心', 'current-menu', 'right')
        
    def parse_program(self, response):
        yield self.__parse(response, '方案与案例', 'current-menu', 'right')     

    def parse_case(self, response):
        yield self.__parse(response, '经典案例', 'detail-title', 'detail-content')

    def parse_news(self, response):
        yield self.__parse(response, '新闻中心', 'detail-title', 'detail-content')

    # def parse_images(self, response):
    #     print('==>', self.name, '-Images-' , response.url)

    def __extract_title(self, response, xpath=None):        
        if xpath is None:
            return ''
        title = response.xpath(xpath).extract_first()
        return title.strip() if title is not None else ''
