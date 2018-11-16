# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HedaItem(scrapy.Item):   
    title = scrapy.Field()
    url = scrapy.Field()
    contents = scrapy.Field()
    words = scrapy.Field()
    article_content = scrapy.Field()
    article_id = scrapy.Field()
    company = scrapy.Field()
