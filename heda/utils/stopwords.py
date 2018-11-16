# -*- coding: utf-8 -*-

STOPWORDS_FILE_LIST = ['utils/stopwords_common.txt', 'utils/stopwords_professional.txt']
STOPWORDS = []
INITIALIZED = False

def load_stopwords(filenames):
    global INITIALIZED
    global STOPWORDS
    if INITIALIZED == False:
        STOPWORDS = get_stopwords(STOPWORDS_FILE_LIST)
        INITIALIZED = True

def get_stopwords(filenames):
    stopwords = []
    for file in filenames:
        stopwords += [line.strip() for line in open(file, 'r', encoding='utf-8').readlines()]  
    return stopwords

def check_stopword(word):
    load_stopwords(STOPWORDS_FILE_LIST)
    return word in STOPWORDS