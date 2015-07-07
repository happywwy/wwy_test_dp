# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 20:44:12 2015

@author: happywwy1991
"""

import cPickle
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()

feature_dic = cPickle.load(open('feature_dic_2', 'r'))
opinion_dic = cPickle.load(open('opinion_dic_2', 'r'))
pruned_feature = open('pruned_feature_2', 'w')
processed_sentence = open('processed_sentence', 'r').read().splitlines()
feature_freq = cPickle.load(open('feature_freq_2', 'r'))
opinion_freq = cPickle.load(open('opinion_freq_2', 'r'))

opinion_word = []
sentiword = open('sentiword', 'r').read().splitlines()
for senti in sentiword:
    word = senti.split(' ')[0]
    opinion_word.append(word)

target_pair_dic = cPickle.load(open('target_pair_2', 'r'))

#extracted_feature = cPickle.load(open('extract_feature', 'r'))

pos_sentence_origin = cPickle.load(open('pos_combine', 'rb'))
pos_sentence = {}
for key in pos_sentence_origin.keys():
    pos_sentence[key] = pos_sentence_origin[key][0]

processed_reviews = cPickle.load(open('processed_parser', 'r'))

nn = ['NN', 'NNS']
jj = ['JJ', 'JJR', 'JJS']

#conj_set = cPickle.load(open('conjunction_set_mod', 'r'))
conj_set = {}

new_feature_dic = {}
for i in range(len(feature_dic)):
    new_feature_dic[i] = feature_dic[i][:]


#separate feature_freq into 5 datasets
canon_freq = {}
nikon_freq = {}
nokia_freq = {}
mp3_freq = {}
dvd_freq = {}

alldata_freq = cPickle.load(open('alldata_feature_freq', 'r'))

#recompute conj_set
for i in range(len(feature_dic)):
    conj_set[i] = []
    for feature in feature_dic[i]:
        feature_ind = [row[1] for row in processed_reviews[i]].index(feature)
        if processed_reviews[i][feature_ind][4] == 'conj':
            dep_ind = processed_reviews[i][feature_ind][3]
            dep_index = [row[0] for row in processed_reviews[i]].index(dep_ind)
            conj_set[i].append([feature, processed_reviews[i][dep_index][1]]) 



for i in range(597):

    for item in feature_dic[i]:
        if wordnet_lemmatizer.lemmatize(item) not in canon_freq.keys():
            canon_freq[wordnet_lemmatizer.lemmatize(item)] = 1
        else:
            canon_freq[wordnet_lemmatizer.lemmatize(item)] += 1
            
    
    
    
            
for i in range(597,943):
    for item in feature_dic[i]:
        if wordnet_lemmatizer.lemmatize(item) not in nikon_freq.keys():
            nikon_freq[wordnet_lemmatizer.lemmatize(item)] = 1
        else:
            nikon_freq[wordnet_lemmatizer.lemmatize(item)] += 1
            
for i in range(943,1489):
    for item in feature_dic[i]:
        if wordnet_lemmatizer.lemmatize(item) not in nokia_freq.keys():
            nokia_freq[wordnet_lemmatizer.lemmatize(item)] = 1
        else:
            nokia_freq[wordnet_lemmatizer.lemmatize(item)] += 1
            
for i in range(1489,3205):
    for item in feature_dic[i]:
        if wordnet_lemmatizer.lemmatize(item) not in mp3_freq.keys():
            mp3_freq[wordnet_lemmatizer.lemmatize(item)] = 1
        else:
            mp3_freq[wordnet_lemmatizer.lemmatize(item)] += 1
            
for i in range(3205,3945):
    for item in feature_dic[i]:
        if wordnet_lemmatizer.lemmatize(item) not in dvd_freq.keys():
            dvd_freq[wordnet_lemmatizer.lemmatize(item)] = 1
        else:
            dvd_freq[wordnet_lemmatizer.lemmatize(item)] += 1



#prune infrequent features  
'''
for i in range(3945):
    for item in feature_dic[i]:
        if feature_freq[wordnet_lemmatizer.lemmatize(item)] <= 1:
            
            for pair in target_pair_dic[i]:
                if item == pair[0]:
                    opinion = pair[1]
                else:
                    opinion = pair[0]
                    
                if opinion in opinion_freq.keys() and opinion_freq[opinion] < 5:
                    for j in range(len(target_pair_dic)):
                        for thing in target_pair_dic[j]:
                            if thing[0] == opinion and thing[1] in feature_dic[j]:
                                feature_dic[j].remove(thing[1])
                            elif thing[1] == opinion and thing[0] in feature_dic[j]:
                                feature_dic[j].remove(thing[0])
           
            feature_dic[i].remove(item)
            feature_freq[wordnet_lemmatizer.lemmatize(item)] -= 1  
''' 

#record the features being kept
mp3_keep = []
nokia_keep = []
           
for i in range(597):
    
    for item in feature_dic[i]:
        if canon_freq[wordnet_lemmatizer.lemmatize(item)] <= 1: #and (alldata_freq[wordnet_lemmatizer.lemmatize(item)] <= 2 \
        or alldata_freq[wordnet_lemmatizer.lemmatize(item)] >= 5):
            print item, i, #target_pair_dic[i],
            new_feature_dic[i].remove(item)
            #canon_freq[wordnet_lemmatizer.lemmatize(item)] -= 2

            
for i in range(597, 943):
    for item in feature_dic[i]:
        if nikon_freq[wordnet_lemmatizer.lemmatize(item)] <= 1:
            new_feature_dic[i].remove(item)
            #nikon_freq[wordnet_lemmatizer.lemmatize(item)] -= 1 
            '''
            for pair in target_pair_dic[i]:
                if item == pair[0]:
                    opinion = pair[1]
                else:
                    opinion = pair[0]
                    
                if opinion in opinion_freq.keys(): #and opinion_freq[opinion] < 5:
                    for j in range(597, 943):
                        for thing in target_pair_dic[j]:
                            if thing[0] == opinion and thing[1] in feature_dic[j]:
                                feature_dic[j].remove(thing[1])
                            elif thing[1] == opinion and thing[0] in feature_dic[j]:
                                feature_dic[j].remove(thing[0])
            '''
for i in range(943, 1489):
    for item in feature_dic[i]:
        if nokia_freq[wordnet_lemmatizer.lemmatize(item)] <= 1:
            new_feature_dic[i].remove(item)
            #nokia_freq[wordnet_lemmatizer.lemmatize(item)] -= 1
            '''
            for pair in target_pair_dic[i]:
                if item == pair[0]:
                    opinion = pair[1]
                else:
                    opinion = pair[0]
                    
                if opinion in opinion_freq.keys(): #and opinion_freq[opinion] < 5:
                    for j in range(943, 1489):
                        for thing in target_pair_dic[j]:
                            if thing[0] == opinion and thing[1] in feature_dic[j]:
                                feature_dic[j].remove(thing[1])
                            elif thing[1] == opinion and thing[0] in feature_dic[j]:
                                feature_dic[j].remove(thing[0])
            '''

for i in range(1489, 3205):
    for item in feature_dic[i]:
        if mp3_freq[wordnet_lemmatizer.lemmatize(item)] <= 1:
            if item not in [row[0] for row in conj_set[i]] and item not in [row[1] for row in conj_set[i]]:
                new_feature_dic[i].remove(item)
            #mp3_freq[wordnet_lemmatizer.lemmatize(item)] -= 1 
            '''
            for pair in target_pair_dic[i]:
                if item == pair[0]:
                    opinion = pair[1]
                else:
                    opinion = pair[0]
                    
                if opinion in opinion_freq.keys(): #and opinion_freq[opinion] < 5:
                    for j in range(1489, 3205):
                        for thing in target_pair_dic[j]:
                            if thing[0] == opinion and thing[1] in feature_dic[j]:
                                feature_dic[j].remove(thing[1])
                            elif thing[1] == opinion and thing[0] in feature_dic[j]:
                                feature_dic[j].remove(thing[0])
            '''

for i in range(3205, 3945):
    for item in feature_dic[i]:
        if dvd_freq[wordnet_lemmatizer.lemmatize(item)] <= 1:
            new_feature_dic[i].remove(item)
            #dvd_freq[wordnet_lemmatizer.lemmatize(item)] -= 1
            '''
            for pair in target_pair_dic[i]:
                if item == pair[0]:
                    opinion = pair[1]
                else:
                    opinion = pair[0]
                    
                if opinion in opinion_freq.keys(): #and opinion_freq[opinion] < 5:
                    for j in range(3205, 3945):
                        for thing in target_pair_dic[j]:
                            if thing[0] == opinion and thing[1] in feature_dic[j]:
                                feature_dic[j].remove(thing[1])
                            elif thing[1] == opinion and thing[0] in feature_dic[j]:
                                feature_dic[j].remove(thing[0])
            '''

#pruning 1: infrequent word in the same clause 
for ind, review in enumerate(processed_reviews):
    if ind < 597:
        count = 0
        feature = []   
        check_first_clause = False
        
        review_accumulate = []
        length = 0
        

        
        #mod_review = review
        
        for item in review:
            length += 1
            
            if item[2][1] != 'C':
                if item[1] in new_feature_dic[ind] and check_first_clause == False:
                    new_feature_dic[ind].remove(item[1])
                    '''
                    if [row[1] for row in mod_review].count(item[1]) < 2:
                        feature_dic[ind].remove(item[1])
                    else:
                        mod_review.remove(item)
                    '''
   
                    #canon_freq[wordnet_lemmatizer.lemmatize(item[1])] -= 1

                elif check_first_clause == True:
                    review_accumulate.append(item)
                    
                    if item[1] in new_feature_dic[ind] and item[1] not in feature:
                    
                        count += 1
                        feature.append(item[1])
    
    
            if item[2][1] == 'C' or length == len(review):
                check_first_clause = True
                
                if count > 1:
                    max_freq = 0
                    for i in range(len(feature)):
                        if canon_freq[wordnet_lemmatizer.lemmatize(feature[i])] >= max_freq:
                            max_freq = canon_freq[wordnet_lemmatizer.lemmatize(feature[i])]
                    for i in range(len(feature)):
                        if conj_set[ind] == []:
                            if canon_freq[wordnet_lemmatizer.lemmatize(feature[i])] != max_freq and feature[i] in new_feature_dic[ind]:
                                if canon_freq[wordnet_lemmatizer.lemmatize(feature[i])] < 5:
                                    new_feature_dic[ind].remove(feature[i])
                                '''
                                if [row[1] for row in mod_review].count(feature[i]) < 2:
                                    feature_dic[ind].remove(feature[i])
                                elif item not in mod_review:
                                    mod_review.remove(item)
                                '''

                                #canon_freq[wordnet_lemmatizer.lemmatize(feature[i])] -= 1
  
                                    
                        
                        else:
                            if canon_freq[wordnet_lemmatizer.lemmatize(feature[i])] != max_freq and feature[i] in new_feature_dic[ind]:
                                if feature[i] not in [row[0] for row in conj_set[ind]]:
                                    if canon_freq[wordnet_lemmatizer.lemmatize(feature[i])] < 5:
                                        new_feature_dic[ind].remove(feature[i])
                                    '''
                                    if [row[1] for row in mod_review].count(feature[i]) < 2:
                                        feature_dic[ind].remove(feature[i])
                                    elif item not in mod_review:
                                        mod_review.remove(item)
                                    '''

                                    #canon_freq[wordnet_lemmatizer.lemmatize(feature[i])] -= 1

                                    
                                else:
                                    indice = [row[0] for row in conj_set[ind]].index(feature[i])
                                    head = conj_set[ind][indice][1]
                                    
                                    if (head in feature and canon_freq[wordnet_lemmatizer.lemmatize(head)] != max_freq) or head not in feature:
                                        if canon_freq[wordnet_lemmatizer.lemmatize(feature[i])] < 5:
                                            new_feature_dic[ind].remove(feature[i])
                                        '''
                                        if [row[1] for row in mod_review].count(feature[i]) < 2:
                                            feature_dic[ind].remove(feature[i])
                                        elif item not in mod_review:
                                            mod_review.remove(item)
                                        '''

                                        #canon_freq[wordnet_lemmatizer.lemmatize(feature[i])] -= 1
              
                #if count = 1 but feature relation is conjunction
                elif count == 1 and feature[0] in new_feature_dic[ind]:
                    if feature[0] in [row[0] for row in conj_set[ind]] and canon_freq[wordnet_lemmatizer.lemmatize(feature[0])] < 5:
                        new_feature_dic[ind].remove(feature[0])
                        

                        #canon_freq[wordnet_lemmatizer.lemmatize(feature[0])] -= 1
                
                
                count = 0
                feature = []
                review_accumulate = []
                
    if ind in range(597, 943):
        count = 0
        feature = []   
        check_first_clause = False
        
        review_accumulate = []
        length = 0
        
        
        #mod_review = review
        
        for item in review:
            length += 1
            
            if item[2][1] != 'C':
                if item[1] in new_feature_dic[ind] and check_first_clause == False:
                    new_feature_dic[ind].remove(item[1])
                    '''
                    if [row[1] for row in mod_review].count(item[1]) < 2:
                        feature_dic[ind].remove(item[1])
                    else:
                        mod_review.remove(item)
                    '''
   
                    #canon_freq[wordnet_lemmatizer.lemmatize(item[1])] -= 1

                elif check_first_clause == True:
                    review_accumulate.append(item)
                    
                    if item[1] in new_feature_dic[ind] and item[1] not in feature:
                    
                        count += 1
                        feature.append(item[1])
    
    
            if item[2][1] == 'C' or length == len(review):
                check_first_clause = True
                
                if count > 1:
                    max_freq = 0
                    for i in range(len(feature)):
                        if nikon_freq[wordnet_lemmatizer.lemmatize(feature[i])] >= max_freq:
                            max_freq = nikon_freq[wordnet_lemmatizer.lemmatize(feature[i])]
                    for i in range(len(feature)):
                        if conj_set[ind] == []:
                            if nikon_freq[wordnet_lemmatizer.lemmatize(feature[i])] != max_freq and feature[i] in new_feature_dic[ind]:
                                if nikon_freq[wordnet_lemmatizer.lemmatize(feature[i])] < 5:
                                    new_feature_dic[ind].remove(feature[i])
                                '''
                                if [row[1] for row in mod_review].count(feature[i]) < 2:
                                    feature_dic[ind].remove(feature[i])
                                elif item not in mod_review:
                                    mod_review.remove(item)
                                '''

                                #canon_freq[wordnet_lemmatizer.lemmatize(feature[i])] -= 1
  
                                    
                        
                        else:
                            if nikon_freq[wordnet_lemmatizer.lemmatize(feature[i])] != max_freq and feature[i] in new_feature_dic[ind]:
                                if feature[i] not in [row[0] for row in conj_set[ind]]:
                                    if nikon_freq[wordnet_lemmatizer.lemmatize(feature[i])] < 5:
                                        new_feature_dic[ind].remove(feature[i])
                                    '''
                                    if [row[1] for row in mod_review].count(feature[i]) < 2:
                                        feature_dic[ind].remove(feature[i])
                                    elif item not in mod_review:
                                        mod_review.remove(item)
                                    '''

                                    #canon_freq[wordnet_lemmatizer.lemmatize(feature[i])] -= 1

                                    
                                else:
                                    indice = [row[0] for row in conj_set[ind]].index(feature[i])
                                    head = conj_set[ind][indice][1]
                                    
                                    if (head in feature and nikon_freq[wordnet_lemmatizer.lemmatize(head)] != max_freq) or head not in feature:
                                        if nikon_freq[wordnet_lemmatizer.lemmatize(feature[i])] < 5:
                                            new_feature_dic[ind].remove(feature[i])
                                        '''
                                        if [row[1] for row in mod_review].count(feature[i]) < 2:
                                            feature_dic[ind].remove(feature[i])
                                        elif item not in mod_review:
                                            mod_review.remove(item)
                                        '''

                                        #canon_freq[wordnet_lemmatizer.lemmatize(feature[i])] -= 1
              
                #if count = 1 but feature relation is conjunction
                elif count == 1 and feature[0] in new_feature_dic[ind]:
                    if feature[0] in [row[0] for row in conj_set[ind]] and nikon_freq[wordnet_lemmatizer.lemmatize(feature[0])] < 5:
                        new_feature_dic[ind].remove(feature[0])
                      

                        #canon_freq[wordnet_lemmatizer.lemmatize(feature[0])] -= 1
                
               
                count = 0
                feature = []
                review_accumulate = []
                
    if ind in range(943, 1489):
        count = 0
        feature = []   
        check_first_clause = False
        
        review_accumulate = []
        length = 0
        

        #mod_review = review
        
        for item in review:
            length += 1
            
            if item[2][1] != 'C':
                if item[1] in new_feature_dic[ind] and check_first_clause == False:
                    new_feature_dic[ind].remove(item[1])
                    '''
                    if [row[1] for row in mod_review].count(item[1]) < 2:
                        feature_dic[ind].remove(item[1])
                    else:
                        mod_review.remove(item)
                    '''
   
                    #canon_freq[wordnet_lemmatizer.lemmatize(item[1])] -= 1

                elif check_first_clause == True:
                    review_accumulate.append(item)
                    
                    if item[1] in new_feature_dic[ind] and item[1] not in feature:
                    
                        count += 1
                        feature.append(item[1])
    
    
            if item[2][1] == 'C' or length == len(review):
                check_first_clause = True
                
                if count > 1:
                    max_freq = 0
                    for i in range(len(feature)):
                        if nokia_freq[wordnet_lemmatizer.lemmatize(feature[i])] >= max_freq:
                            max_freq = nokia_freq[wordnet_lemmatizer.lemmatize(feature[i])]
                    for i in range(len(feature)):
                        if conj_set[ind] == []:
                            if nokia_freq[wordnet_lemmatizer.lemmatize(feature[i])] != max_freq and feature[i] in new_feature_dic[ind]:
                                if nokia_freq[wordnet_lemmatizer.lemmatize(feature[i])] < 5:
                                    new_feature_dic[ind].remove(feature[i])
                                '''
                                if [row[1] for row in mod_review].count(feature[i]) < 2:
                                    feature_dic[ind].remove(feature[i])
                                elif item not in mod_review:
                                    mod_review.remove(item)
                                '''

                                #canon_freq[wordnet_lemmatizer.lemmatize(feature[i])] -= 1
  
                        else:
                            if nokia_freq[wordnet_lemmatizer.lemmatize(feature[i])] != max_freq and feature[i] in new_feature_dic[ind]:
                                if feature[i] not in [row[0] for row in conj_set[ind]] and feature[i] not in [row[1] for row in conj_set[ind]]:
                                    new_feature_dic[ind].remove(feature[i])
                           

                                elif feature[i] in [row[0] for row in conj_set[ind]]:
                                    indice = [row[0] for row in conj_set[ind]].index(feature[i])
                                    head = conj_set[ind][indice][1]
                                    
                                    if (head in feature and nokia_freq[wordnet_lemmatizer.lemmatize(head)] != max_freq) or head not in feature:
                                        new_feature_dic[ind].remove(feature[i])
                                    else:
                                        nokia_keep.append(feature[i])
                                        
                                else:
                                    indice = [row[1] for row in conj_set[ind]].index(feature[i])
                                    tail = conj_set[ind][indice][0]
                                    
                                    if (tail in feature and nokia_freq[wordnet_lemmatizer.lemmatize(tail)] != max_freq) or tail not in feature:
                                        new_feature_dic[ind].remove(feature[i])
                                    else:
                                        nokia_keep.append(feature[i])            
                        '''
                        else:
                            if nokia_freq[wordnet_lemmatizer.lemmatize(feature[i])] != max_freq and feature[i] in new_feature_dic[ind]:
                                if feature[i] not in [row[0] for row in conj_set[ind]]:
                                    if nokia_freq[wordnet_lemmatizer.lemmatize(feature[i])] < 5:
                                        new_feature_dic[ind].remove(feature[i])
                        

                                    #canon_freq[wordnet_lemmatizer.lemmatize(feature[i])] -= 1

                                    
                                else:
                                    indice = [row[0] for row in conj_set[ind]].index(feature[i])
                                    head = conj_set[ind][indice][1]
                                    
                                    if (head in feature and nokia_freq[wordnet_lemmatizer.lemmatize(head)] != max_freq) or head not in feature:
                                        if nokia_freq[wordnet_lemmatizer.lemmatize(feature[i])] < 5:
                                            new_feature_dic[ind].remove(feature[i])
                                      

                                        #canon_freq[wordnet_lemmatizer.lemmatize(feature[i])] -= 1
                        '''
                
                #if count = 1 but feature relation is conjunction
                elif count == 1 and feature[0] in new_feature_dic[ind]:
                    if feature[0] in [row[0] for row in conj_set[ind]] and nokia_freq[wordnet_lemmatizer.lemmatize(feature[0])] < 5:
                        new_feature_dic[ind].remove(feature[0])
                        

                        #canon_freq[wordnet_lemmatizer.lemmatize(feature[0])] -= 1
                
                
                count = 0
                feature = []
                review_accumulate = []
                
                
    if ind in range(1489, 3205):
        count = 0
        feature = []   
        check_first_clause = False
        
        review_accumulate = []
        length = 0
        
        if ind == 1790:
            check = True
        
        #mod_review = review
        
        for item in review:
            length += 1
            
            if item[2][1] != 'C':
                if item[1] in new_feature_dic[ind] and check_first_clause == False:
                    new_feature_dic[ind].remove(item[1])
                    '''
                    if [row[1] for row in mod_review].count(item[1]) < 2:
                        feature_dic[ind].remove(item[1])
                    else:
                        mod_review.remove(item)
                    '''
   
                    #canon_freq[wordnet_lemmatizer.lemmatize(item[1])] -= 1

                elif check_first_clause == True:
                    review_accumulate.append(item)
                    
                    if item[1] in new_feature_dic[ind] and item[1] not in feature:
                    
                        count += 1
                        feature.append(item[1])
    
    
            if item[2][1] == 'C' or length == len(review):
                check_first_clause = True
                
                if count > 1:
                    max_freq = 0
                    for i in range(len(feature)):
                        if mp3_freq[wordnet_lemmatizer.lemmatize(feature[i])] >= max_freq:
                            max_freq = mp3_freq[wordnet_lemmatizer.lemmatize(feature[i])]
                    for i in range(len(feature)):
                        if conj_set[ind] == []:
                            if mp3_freq[wordnet_lemmatizer.lemmatize(feature[i])] != max_freq and feature[i] in new_feature_dic[ind]:
                                new_feature_dic[ind].remove(feature[i])
                                '''
                                if [row[1] for row in mod_review].count(feature[i]) < 2:
                                    feature_dic[ind].remove(feature[i])
                                elif item not in mod_review:
                                    mod_review.remove(item)
                                '''

                                #canon_freq[wordnet_lemmatizer.lemmatize(feature[i])] -= 1
  
                                    
                        
                        else:
                            if mp3_freq[wordnet_lemmatizer.lemmatize(feature[i])] != max_freq and feature[i] in new_feature_dic[ind]:
                                if feature[i] not in [row[0] for row in conj_set[ind]] and feature[i] not in [row[1] for row in conj_set[ind]]:
                                    new_feature_dic[ind].remove(feature[i])
                           

                                elif feature[i] in [row[0] for row in conj_set[ind]]:
                                    indice = [row[0] for row in conj_set[ind]].index(feature[i])
                                    head = conj_set[ind][indice][1]
                                    
                                    if (head in feature and mp3_freq[wordnet_lemmatizer.lemmatize(head)] != max_freq) or head not in feature:
                                        new_feature_dic[ind].remove(feature[i])
                                    else:
                                        mp3_keep.append(feature[i])
                                        
                                else:
                                    indice = [row[1] for row in conj_set[ind]].index(feature[i])
                                    tail = conj_set[ind][indice][0]
                                    
                                    if (tail in feature and mp3_freq[wordnet_lemmatizer.lemmatize(tail)] != max_freq) or tail not in feature:
                                        new_feature_dic[ind].remove(feature[i])
                                    else:
                                        mp3_keep.append(feature[i])

                                '''    
                                else:
                                    indice = [row[0] for row in conj_set[ind]].index(feature[i])
                                    head = conj_set[ind][indice][1]
                                    
                                    if (head in feature and mp3_freq[wordnet_lemmatizer.lemmatize(head)] != max_freq) or head not in feature:
                                        new_feature_dic[ind].remove(feature[i])
                     
                                    else:
                                        mp3_keep.append(feature[i])
                                '''

                                        #canon_freq[wordnet_lemmatizer.lemmatize(feature[i])] -= 1
               
                #if count = 1 but feature relation is conjunction
                elif count == 1 and feature[0] in new_feature_dic[ind]:
                    if feature[0] in [row[0] for row in conj_set[ind]]:
                        new_feature_dic[ind].remove(feature[0])
                        
                        #canon_freq[wordnet_lemmatizer.lemmatize(feature[0])] -= 1
                
                
                count = 0
                feature = []
                review_accumulate = []
                
    if ind in range(3205, 3945):
        count = 0
        feature = []   
        check_first_clause = False
        
        review_accumulate = []
        length = 0
        
        
        #mod_review = review
        
        for item in review:
            length += 1
            
            if item[2][1] != 'C':
                if item[1] in new_feature_dic[ind] and check_first_clause == False:
                    new_feature_dic[ind].remove(item[1])
                    '''
                    if [row[1] for row in mod_review].count(item[1]) < 2:
                        feature_dic[ind].remove(item[1])
                    else:
                        mod_review.remove(item)
                    '''
   
                    #canon_freq[wordnet_lemmatizer.lemmatize(item[1])] -= 1

                elif check_first_clause == True:
                    review_accumulate.append(item)
                    
                    if item[1] in new_feature_dic[ind] and item[1] not in feature:
                    
                        count += 1
                        feature.append(item[1])
    
    
            if item[2][1] == 'C' or length == len(review):
                check_first_clause = True
                
                if count > 1:
                    max_freq = 0
                    for i in range(len(feature)):
                        if dvd_freq[wordnet_lemmatizer.lemmatize(feature[i])] >= max_freq:
                            max_freq = dvd_freq[wordnet_lemmatizer.lemmatize(feature[i])]
                    for i in range(len(feature)):
                        if conj_set[ind] == []:
                            if dvd_freq[wordnet_lemmatizer.lemmatize(feature[i])] != max_freq and feature[i] in new_feature_dic[ind]:
                                new_feature_dic[ind].remove(feature[i])
                                '''
                                if [row[1] for row in mod_review].count(feature[i]) < 2:
                                    feature_dic[ind].remove(feature[i])
                                elif item not in mod_review:
                                    mod_review.remove(item)
                                '''

                                #canon_freq[wordnet_lemmatizer.lemmatize(feature[i])] -= 1
  
                                    
                        
                        else:
                            if dvd_freq[wordnet_lemmatizer.lemmatize(feature[i])] != max_freq and feature[i] in new_feature_dic[ind]:
                                if feature[i] not in [row[0] for row in conj_set[ind]]:
                                    new_feature_dic[ind].remove(feature[i])
                                    '''
                                    if [row[1] for row in mod_review].count(feature[i]) < 2:
                                        feature_dic[ind].remove(feature[i])
                                    elif item not in mod_review:
                                        mod_review.remove(item)
                                    '''

                                    #canon_freq[wordnet_lemmatizer.lemmatize(feature[i])] -= 1

                                    
                                else:
                                    indice = [row[0] for row in conj_set[ind]].index(feature[i])
                                    head = conj_set[ind][indice][1]
                                    
                                    if (head in feature and dvd_freq[wordnet_lemmatizer.lemmatize(head)] != max_freq) or head not in feature:
                                        new_feature_dic[ind].remove(feature[i])
                                        '''
                                        if [row[1] for row in mod_review].count(feature[i]) < 2:
                                            feature_dic[ind].remove(feature[i])
                                        elif item not in mod_review:
                                            mod_review.remove(item)
                                        '''

                                        #canon_freq[wordnet_lemmatizer.lemmatize(feature[i])] -= 1
                
                #if count = 1 but feature relation is conjunction
                elif count == 1 and feature[0] in new_feature_dic[ind]:
                    if feature[0] in [row[0] for row in conj_set[ind]]:
                        new_feature_dic[ind].remove(feature[0])
                       
                        #canon_freq[wordnet_lemmatizer.lemmatize(feature[0])] -= 1
                
                
                count = 0
                feature = []
                review_accumulate = []

'''
#delete less frequent opinion word and corresponding features
#prune features with opinion not in seed
for i in range(3945):
    for pair in target_pair_dic[i]:
        
        if pair[1] in opinion_freq.keys() and opinion_freq[pair[1]] <= 3:
            #opinion_freq.keys().remove(pair[1])   
            feature = pair[0]
            if feature in new_feature_dic[i]:
                new_feature_dic[i].remove(feature)
                #canon_freq[wordnet_lemmatizer.lemmatize(feature)] -= 1
                
        elif pair[0] in opinion_freq.keys() and opinion_freq[pair[0]] <= 3:
            feature = pair[1]
                
            if feature in new_feature_dic[i]:
                new_feature_dic[i].remove(feature)
                #canon_freq[wordnet_lemmatizer.lemmatize(feature)] -= 1
       
               
        if pair[0] in opinion_freq.keys() and pair[0] not in opinion_word:
            if pair[1] in new_feature_dic[i]:
                new_feature_dic[i].remove(pair[1])
        elif pair[1] in opinion_freq.keys() and pair[1] not in opinion_word:
            if pair[0] in new_feature_dic[i]:
                new_feature_dic[i].remove(pair[0])
'''       


final_feature_dic = {}
for i in range(3945):
    final_feature_dic[i] = new_feature_dic[i][:]


for i in range(597):
    for item in new_feature_dic[i]:
        if canon_freq[wordnet_lemmatizer.lemmatize(item)] <= 3: #and (alldata_freq[wordnet_lemmatizer.lemmatize(item)] <= 2 \
        or alldata_freq[wordnet_lemmatizer.lemmatize(item)] >= 5):
            final_feature_dic[i].remove(item)

           
for i in range(597, 943):
    for item in new_feature_dic[i]:
        if nikon_freq[wordnet_lemmatizer.lemmatize(item)] <= 3:
            final_feature_dic[i].remove(item)

for i in range(943, 1489):
    for item in new_feature_dic[i]:
        if nokia_freq[wordnet_lemmatizer.lemmatize(item)] <= 2: #and item not in nokia_keep:
            final_feature_dic[i].remove(item)
            
for i in range(1489, 3205):
    for item in new_feature_dic[i]:
        if mp3_freq[wordnet_lemmatizer.lemmatize(item)] <= 3: #4 and item not in mp3_keep:
            final_feature_dic[i].remove(item)
            
for i in range(3205, 3945):
    for item in new_feature_dic[i]:
        if dvd_freq[wordnet_lemmatizer.lemmatize(item)] <= 3:
            final_feature_dic[i].remove(item)

'''
#prune features after 'better than' or 'as'
#prune selected features that are in the bracket
for ind, review in enumerate(processed_reviews):
    if ind in range(1489, 3205):
    
        inside_bracket = False
        for item in review:
            
            if item[1] == '(':
                inside_bracket = True
            elif item[1] == ')':
                inside_bracket == False
            
            if item[1] in new_feature_dic[ind] and inside_bracket == True:
                new_feature_dic[ind].remove(item[1])
                
            if item[1] in new_feature_dic[ind] and len(item) > 5:
                if item[5] == '(gov as)' or item[5] == '(gov than)':
                    new_feature_dic[ind].remove(item[1])



for i in range(1489, 3205):
    for item in new_feature_dic[i]:
        if mp3_freq[wordnet_lemmatizer.lemmatize(item)] <= 3:
            new_feature_dic[i].remove(item)
'''
for i in range(len(final_feature_dic)):
    pruned_feature.write(''.join(word + ' ' for word in final_feature_dic[i]))
    pruned_feature.write('\n')
    
pruned_feature.close()   

pruned_feature_dic = cPickle.dump(final_feature_dic, open('pruned_feature_dic_2', 'w'))