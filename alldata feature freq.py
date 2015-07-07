# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 15:43:13 2015

@author: wangwenya
"""

import cPickle
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()

feature_freq = cPickle.load(open('feature_freq_2', 'r'))

pos_sentence_origin = cPickle.load(open('pos_combine', 'rb'))
pos_sentence = {}
for key in pos_sentence_origin.keys():
    pos_sentence[key] = pos_sentence_origin[key][0]

alldata_freq = {}

#record alldata frequency
for i in range(3945):
    for item in pos_sentence[i]:
        if wordnet_lemmatizer.lemmatize(item[0]) in feature_freq.keys():
            if wordnet_lemmatizer.lemmatize(item[0]) in alldata_freq.keys():
                alldata_freq[wordnet_lemmatizer.lemmatize(item[0])] += 1
            else:
                alldata_freq[wordnet_lemmatizer.lemmatize(item[0])] = 1


cPickle.dump(alldata_freq, open('alldata_feature_freq', 'w'))