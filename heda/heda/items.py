# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ContentItem(scrapy.Item):   
    title = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    company = scrapy.Field()
    words = scrapy.Field()
    article_id = scrapy.Field()