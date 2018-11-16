# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
import jieba
from elasticsearch import Elasticsearch

class HedaSegmentPipeline(object):

    def __init__(self):
        jieba.load_userdict('dict.txt')
        self.stopwords = self.stopwordslist()

    def stopwordslist(self):  
        stopwords = [line.strip() for line in open('stopwords.txt', 'r', encoding='utf-8').readlines()]  
        return stopwords        

    def process_item(self, item, spider):

        NUMBER_PATTERN = re.compile(r'^[A-Za-z0-9.%~]+$')

        words = []
        for content in item['contents']:
            content = content.strip()
            if len(content) > 0:
                iterword = jieba.cut(content)
                for word in iterword:
                    word_ = word.strip()
                    if len(word_) <= 1: continue
                    if NUMBER_PATTERN.search(word_) is not None: continue
                    if word_ in self.stopwords: continue
                    words.append(word_)

        print('==>', len(set(words)))

        item['words'] = set(words)
        return item

class HedaArticlePipeline(object):

    def __init__(self):
        self.es = Elasticsearch('128.1.6.45:9200', timeout=5000)

    def process_item(self, item, spider):
        content = '\r\n'.join([''.join(c.split()) for c in item['contents']])
        res = self.es.index(index='cia_article', doc_type="heda", body={
            'content': content
        })
        item['article_content'] = content
        item['article_id'] = res['_id']
        return item

class HedaInvertedIndexPipeline(object):

    def __init__(self):        
        self.es = Elasticsearch('128.1.6.45:9200', timeout=5000)

    def process_item(self, item, spider):    

        if not self.es.indices.exists('cia_word'):
            # self.es.indices.delete('cia_word')
            self.es.indices.create('cia_word')

        for word in item['words']:          
            doc = {
                "script" : {
                    "inline": "ctx._source.article_id.add(params.article_id); ctx._source.freq += 1;",
                    "lang": "painless",
                    "params" : {
                        "article_id" : item['article_id']
                    }
                },
                "query": {
                    'constant_score': {
                        "filter" : {
                            "term" : { 
                                'key_word': word
                            }
                        }   
                    }                    
                }
            }

            res = self.es.update_by_query(index='cia_word', doc_type="heda", body=doc)
            # print('==>', word, res['updated'])

            if res['updated'] == 0:
                doc = {
                    "key_word": word,
                    "freq": 1,
                    "article_id": [ item['article_id'] ],
                    "source": item['url']                    
                }

                res = self.es.index(index='cia_word', doc_type="heda", body=doc)        