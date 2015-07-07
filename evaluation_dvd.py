# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 23:02:12 2015

@author: wangwenya
"""
from nltk.stem import WordNetLemmatizer
import numpy as np
import cPickle

wordnet_lemmatizer = WordNetLemmatizer()

review = open('combine_review', 'r').read().splitlines()
feature_output = cPickle.load(open('pruned_feature_dic_2', 'r'))
feature_freq = cPickle.load(open('feature_freq_2', 'r'))


canon_review = review[:597]
nikon_review = review[597:943]
nokia_review = review[943:1489]
mp3_review = review[1489:3205]
dvd_review = review[3205:3945]

canon_predict = [feature_output[i] for i in range(597)]
nikon_predict = [feature_output[i] for i in range(597,943)]
nokia_predict = [feature_output[i] for i in range(943,1489)]
mp3_predict = [feature_output[i] for i in range(1489,3205)]
dvd_predict = [feature_output[i] for i in range(3205,3945)]

feature_set = []
output_set = []
phrase_set = []

canon_feature = []
nikon_feature = []
nokia_feature = []
mp3_feature = []
dvd_feature = []

canon_output = []
nikon_output = []
nokia_output = []
mp3_output = []
dvd_output = []

canon_phrase = []
nikon_phrase = []
nokia_phrase = []
mp3_phrase = []
dvd_phrase = []

vb = ['VB', 'VBD', 'VBP', 'VBG', 'VBN', 'VBZ']

pos_sentence_origin = cPickle.load(open('pos_combine', 'rb'))
pos_sentence = {}
for key in pos_sentence_origin.keys():
    pos_sentence[key] = pos_sentence_origin[key][0]

feature_set = []
for i in range(len(feature_output)):
    for item in feature_output[i]:
        if wordnet_lemmatizer.lemmatize(item) not in feature_set:
            feature_set.append(wordnet_lemmatizer.lemmatize(item))

confusion = np.zeros((2,2))

for ind, line in enumerate(dvd_review):
    line = line.split('##')
    features = line[0].strip()
    

    features = features.split(',')
    
    for feature in features:
        if '[p]' in feature or '[u]' in feature:
           continue

        feature = feature.strip()
        feature = feature.split('[')
        
        #delete features which are verbs
        count_verb = 0
        include = True
        
        if ' ' not in feature[0]:
            if feature[0] in [row[0] for row in pos_sentence[3205 + ind]]:
                indice = [row[0] for row in pos_sentence[3205 + ind]].index(feature[0])
                if pos_sentence[3205 + ind][indice][1] in vb:
                    count_verb += 1
                    include = False
                   
            else:
                for term in [row[0] for row in pos_sentence[3205 + ind]]:
                    indice = [row[0] for row in pos_sentence[3205 + ind]].index(term)
                    if wordnet_lemmatizer.lemmatize(term) == feature[0] and pos_sentence[3205 + ind][indice][1] in vb:
                        count_verb += 1
                        include = False
                        
        else:
            words = feature[0].split(' ')
            for word in words:
                if word in [row[0] for row in pos_sentence[3205 + ind]]:
                    indice = [row[0] for row in pos_sentence[3205 + ind]].index(word)
                    if pos_sentence[3205 + ind][indice][1] in vb:
                        count_verb += 1
                        include = False
                        break
                else:
                    for term in [row[0] for row in pos_sentence[3205 + ind]]:
                        if wordnet_lemmatizer.lemmatize(term) == word:
                            indice = [row[0] for row in pos_sentence[3205 + ind]].index(term)
                            if pos_sentence[3205 + ind][indice][1] in vb:
                                count_verb += 1
                                include = False
                                break
        
        '''
        #feature = feature[0].split(' ')
        terms = feature[0].split(' ')
        if len(terms) > 1:
            processed_feature = ''
            for term in terms:
                feat_word = wordnet_lemmatizer.lemmatize(term)
                processed_feature = processed_feature + feat_word + ' '
            processed_feature = processed_feature.strip()
            if processed_feature not in canon_feature:
                canon_phrase.append(processed_feature)
        else:
            processed_feature = wordnet_lemmatizer.lemmatize(terms[0])
            
        if processed_feature not in canon_feature:
            canon_feature.append(processed_feature)
        '''
                
        
        if wordnet_lemmatizer.lemmatize(feature[0]) not in dvd_feature and include == True:
            dvd_feature.append(wordnet_lemmatizer.lemmatize(feature[0]))
            
    if count_verb == len(features):
        feature_output[ind] = []

dvd_phrase = [] 
phrase_count = 0 
phrase_set = []          
for item in dvd_feature:
    if ' ' in item:
        phrase_count += 1
        phrase_set.append(item)
        item = item.split(' ')
        for word in item:
            if word not in dvd_phrase:
                dvd_phrase.append(word)
                
print phrase_count
        
'''
for line in canon_predict:
    line = line.strip()
    
    line = line.split(' ')
    for term in line:
        term = wordnet_lemmatizer.lemmatize(term)
        if term not in canon_output:
            term = term.encode("utf-8")
            canon_output.append(term)

phrase_word = []
for phrase in canon_phrase:
    phrase = phrase.split(' ')
    for word in phrase:
        if word not in phrase_word:
            phrase_word.append(word)

      
for word in canon_output:
    if word in canon_feature:
        confusion[0][0] += 1
    elif word in phrase_word:
        confusion[0][0] += 1
    else:
        confusion[1][0] += 1
        #print word,
        
for item in canon_feature:
    if ' ' not in item and item not in canon_output:
        confusion[0][1] += 1

for item in canon_phrase:
    item = item.split(' ')
    counter = 0
    for word in item:
        if word in canon_output:
            counter += 1
    if counter == 0:
        confusion[0][1] += 1
'''

for line in dvd_predict:
    if line != '':
        for item in line:
            item = wordnet_lemmatizer.lemmatize(item)
            if item not in dvd_output:
                dvd_output.append(item)
'''
for item in canon_output:
    if item in canon_feature:
        confusion[0][0] += 1
        #print item,
    else:
        confusion[1][0] += 1
        
#print '\n'

for item in canon_feature:
    if item not in canon_output:
        confusion[0][1] += 1

''' 

#count word when it is in a phrase           
for item in dvd_output:
    if item not in dvd_feature and item not in dvd_phrase:
        confusion[1][0] += 1
        print item, dvd_freq[wordnet_lemmatizer.lemmatize(item)],
        
print '\n'

for item in dvd_feature:
    if wordnet_lemmatizer.lemmatize(item) in feature_set:
        confusion[0][0] += 1
    elif ' ' in item:
        contain = False
        item = item.split(' ')
        for word in item:
            if wordnet_lemmatizer.lemmatize(word) in feature_set:
                confusion[0][0] += 1
                contain = True
                break
            
        if contain == False:
            confusion[0][1] += 1
            print item, 
    else:
        confusion[0][1] += 1
        print item, 
print '\n'        

'''
#phrase not counted
for item in canon_output:
    if item not in canon_feature:
        confusion[1][0] += 1
for item in canon_feature:
    if item not in phrase_set:
        if item in feature_set:
            confusion[0][0] += 1
        else:
            confusion[0][1] += 1
'''
        
precision = float(confusion[0][0]) / (confusion[0][0] + confusion[1][0])
recall = float(confusion[0][0]) / (confusion[0][0] + confusion[0][1])
F_score = 2 * recall * precision / (recall + precision)

#print feature_set
#print output_set

print confusion
print "precision: ", precision
print "recall: ", recall
print "F_score: ", F_score
'''
print canon_output
print canon_feature
'''