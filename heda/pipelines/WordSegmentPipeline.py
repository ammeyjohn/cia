# -*- coding: utf-8 -*-

import re
import jieba
from utils.stopwords import check_stopword

# 判断英文、数字、小数点、正负号、%
SKIP_PATTERN = re.compile(r'^[-/+A-Za-z0-9.%]+$')

class WordSegmentPipeline(object):

    def __init__(self):
        jieba.load_userdict('pipelines/dict.txt')

    def process_item(self, item, spider):
        words = set()     
        iterword = jieba.cut(item['content'])
        for word in iterword:
            word_ = word.strip()
            if len(word_) <= 1: continue
            if SKIP_PATTERN.search(word_) is not None: continue
            if check_stopword(word): continue
            words.add(word_)
        item['words'] = words
        print('>>>>> Pipeline:WordSegment', 'Word count =', len(words))
        return item