
# -*- coding: utf-8 -*-

import redis

class UrlCachePipeline(object): 
 
    def open_spider(self, spider):
        pool = redis.ConnectionPool(host='128.1.6.45', port=6379, decode_responses=True)
        self.redis = redis.Redis(connection_pool=pool)            

    def process_item(self, item, spider):
        cache_key = 'uri:url:{0}'.format(item['url'])
        self.redis.set(cache_key, item['url'])
        return item