
# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch

class ESWordWriterPipeline(object):  

    def open_spider(self, spider):
        self.client = Elasticsearch('128.1.6.45:9200', timeout=5000)

        if not self.client.indices.exists(index='cia_word'):
            ret = self.client.indices.create(index='cia_word', body={
                "mappings": {
                    "heda": {
                        "properties": {
                            "word": {"type": "keyword"},                            
                            "freq": {"type": "integer"},
                            "article_ids": {"type": "keyword"}
                        }
                    }
                }
            })
            if ret['acknowledged'] == True:
                print('>>>>> Pipeline:ESWordWriter', 'Index cia_word created')        

    def process_item(self, item, spider):
        
        for word in item['words']:
            doc = {
                "script" : {
                    "inline": "ctx._source.article_ids.add(params.article_id); ctx._source.freq += 1;",
                    "lang": "painless",
                    "params" : {
                        "article_id" : item['article_id']
                    }
                },
                "query": {
                    "term" : { 
                        'word': word
                    }                
                }
            }
            res = self.client.update_by_query(index='cia_word', doc_type="heda", body=doc)            

            if res['updated'] == 0:
                doc = {
                    "word": word,
                    "freq": 1,
                    "article_ids": [ item['article_id'] ]                                     
                }
                res = self.client.index(index='cia_word', doc_type="heda", body=doc)
            #     print('>>>>> Pipeline:ESWordWriter', 'Word', word, 'created')
            # else:
            #     print('>>>>> Pipeline:ESWordWriter', 'Update word', word)  
            
        return item                     