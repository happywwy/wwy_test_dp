# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 20:48:18 2015

@author: happywwy1991
"""
import cPickle

parsed = open('combine_parsed' ,'r').read()

processed_reviews = []

reviews = parsed.split('> (')
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
        
processed = cPickle.dump(processed_reviews, open('processed_parser', 'w'))

processed_sentence = open('processed_sentence', 'w')

for sentence in processed_reviews:
    combine_word = ''
    for row in sentence:
        if 'E' not in row[0]:
            combine_word = combine_word + row[1] + ' '
    processed_sentence.write(combine_word.strip())
    processed_sentence.write('\n')
    
processed_sentence.close()

    