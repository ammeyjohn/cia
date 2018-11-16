
# -*- coding: utf-8 -*-

from datetime import datetime
from elasticsearch import Elasticsearch


class ESArticleWriterPipeline(object):  

    def open_spider(self, spider):
        self.client = Elasticsearch('128.1.6.45:9200', timeout=5000)

        if not self.client.indices.exists(index='cia_article'):
            ret = self.client.indices.create(index='cia_article', body={
                "mappings": {
                    "heda": {
                        "properties": {
                            "content": {"type": "text", "index": "true"},
                            "title": {"type": "text", "index": "true"},
                            "url": {"type": "keyword"},
                            "date": {"type": "date", "format":"YYYY-MM-dd HH:mm:ss"}
                        }
                    }
                }
            })
            if ret['acknowledged'] == True:
                print('>>>>> Pipeline:ESArticleWriter', 'Index cia_article created')

    def process_item(self, item, spider):

        existed = self.client.search(index='cia_article', doc_type='heda', body={
            'query': {
                'match': {
                    'url': item['url']
                }
            }
        })

        article_id = None
        if existed['hits']['total'] == 0:
            res = self.client.index(index='cia_article', doc_type='heda', body={
                'title': item['title'],
                'content': item['content'],
                'url': item['url'],
                'date': str(datetime.now())[:19]
            })
            article_id = res['_id']
        else:
            article_id = existed['hits']['hits'][0]['_id']        
        item['article_id'] = article_id
        return item