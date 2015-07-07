# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 15:24:10 2015

@author: wangwenya
"""

import nltk
'''
import os
java_path = "C:/Program Files/Java/jdk1.8.0_40/bin/java.exe"
os.environ['JAVAHOME'] = java_path
'''

from nltk.tag.stanford import POSTagger
import cPickle

english_postagger = POSTagger('models/english-bidirectional-distsim.tagger', 'stanford-postagger.jar')

parsed = open('combine_parsed' ,'r').read()
reviews = parsed.split('> (')

processed_reviews = []
pos_sentence = {}

for review in reviews:
    if review != '':
        review = review.strip()[:-1]
        review = review.split('\n')[:-1]
        
        processed_items = []
        for item in review:

            item = item.split('\t')
            item[1] = item[1][1:]
            item[-1] = item[-1][:-1]
            item[2] = item[2].split(' ')
            
            processed_items.append(item)
            
        processed_reviews.append(processed_items)
        
for ind, review in enumerate(processed_reviews):
    tokens = []
    for item in review:
        if item[0][0] != 'E':
            tokens.append(item[1])
    pos_sentence[ind] = english_postagger.tag(tokens)
    
postagger = cPickle.dump(pos_sentence, open('pos_combine', 'wb'))   