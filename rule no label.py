# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 22:53:26 2015

@author: wangwenya
"""

import cPickle
from nltk.stem import WordNetLemmatizer

wordnet_lemmatizer = WordNetLemmatizer()


parsed = open('combine_parsed' ,'r').read()
sentiword = open('sentiword', 'r').read().splitlines()
combine_review = open('combine_review', 'r').read().splitlines()


processed_reviews = cPickle.load(open('processed_parser', 'r'))
processed_sentiwords = []

extracted_feature = []
review_feature = {}
review_opinion = {}

target_pair = {}

feature_freq = {}
opinion_freq = {}
pos_sentence_origin = cPickle.load(open('pos_combine', 'rb'))

pos_sentence = {}
for key in pos_sentence_origin.keys():
    pos_sentence[key] = pos_sentence_origin[key][0]

dep = ['mod', 'pnmod', 'subj', 's', 'obj', 'obj2', 'desc', 'mod-before', 'subj-in', 'subj-about', 'subj-because', 'subj-by', 'subj-on', \
'subj-with', 'subj-to', 'subj-out', 'subj-as', 'subj-for', 'subj-around', 'subj-like', 'subj-at', 'subj-through', 'subj-without', \
'subj-after', 'subj-from', 'subj-of', 'subj-because of', 'subj-near', 'subj-than', 'subj-up']
nn = ['NN', 'NNS']
jj = ['JJ', 'JJR', 'JJS']
mods = ['mod', 'pnmod']
sobj = ['s', 'sub', 'obj']

punc = ['(', ')', '.', ',', '-', ':', ';', '!', '?', '%', '\'', '"']

no_label = []

for ind, line in enumerate(combine_review):
    if line[0] == '#':
        no_label.append(ind)
    
    else:    
        line = line.split('##')

        labels = line[0].split(',')
        number = len(labels)
        count = 0
        for label in labels:
            if '[p]' in label or '[u]' in label:
                count += 1
        if count == number and ind not in no_label:
            no_label.append(ind)
    

conj_set = {}

'''
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
'''             

for senti in sentiword:
    word = senti.split(' ')[0]
    processed_sentiwords.append(word)
    
#check if termination condition is met
terminate = False
counter = 0

for ind, review in enumerate(processed_reviews):
    review_feature[ind] = []
    review_opinion[ind] = []
    target_pair[ind] = []
    conj_set[ind] = []

while (terminate == False):
    terminate = True
    counter += 1
    print counter,
    
    for ind, review in enumerate(processed_reviews):
        if ind not in no_label:

            for item in review:
                rel = item[4]
                dep_indice = item[3]
                word = item[1]
                indice = item[0]
                '''
                #if word in feature set, record it in
                if word in extracted_feature and word not in review_feature[ind]:
                    review_feature[ind].append(word)
                    terminate = False
                elif word in processed_sentiwords and word not in review_opinion[ind]:
                    review_opinion[ind].append(word)
                    terminate = False
                '''
                #deal with E~
                if word == '()':
                    origin = item[2][0].lower()
                    for thing in review:
                        if thing != item and (origin == thing[1] or origin == thing[2][0]):
                            word = thing[1]
                            indice = thing[0]
                
                if word in processed_sentiwords and dep_indice[0] != 'E':
                    #extract feature words from opinion seed according to rel1.1 and rel1.2
                    if rel in dep:
                        
                        target = pos_sentence[ind][int(dep_indice) - 1][0]
                        target_pos = pos_sentence[ind][int(dep_indice) - 1][1]
                        #relation R1.1
                        if target_pos in nn and target not in review_feature[ind] and target not in punc:
                            review_feature[ind].append(target)
                            terminate = False
                            
                            target_pair[ind].append([target, word])
                            
                            if target not in extracted_feature:
                                extracted_feature.append(target)
                            #record the frequency of each lemmatized feature
                            if wordnet_lemmatizer.lemmatize(target) not in feature_freq.keys():
                                feature_freq[wordnet_lemmatizer.lemmatize(target)] = 1
                            else:
                                feature_freq[wordnet_lemmatizer.lemmatize(target)] += 1
                            
                        #relation R1.2 
                        for line in review:
                            #deal with E~
                            target_2 = line[1]
                            target_2_ind = line[0]
                            if target_2 == '()':
                                origin_2 = line[2][0].lower()
                                for thing in review:
                                    if thing != line and (origin_2 == thing[1] or origin_2 == thing[2][0]):
                                        target_2 = thing[1]
                                        target_2_ind = thing[0]
                            if line != item and line[3] == dep_indice and target_2_ind[0] != 'E':
                                rel_2 = line[4]
                                if rel_2 in dep:
                                    target_2_pos = pos_sentence[ind][int(target_2_ind) - 1][1]
                                    if target_2_pos in nn and target_2 not in review_feature[ind] and target_2 not in punc:
                                        review_feature[ind].append(target_2)
                                        terminate = False
                                        
                                        target_pair[ind].append([target_2, word])
                                        
                                        if target_2 not in extracted_feature:
                                            extracted_feature.append(target_2)
                                            
                                        #record the frequency of each lemmatized feature
                                        if wordnet_lemmatizer.lemmatize(target_2) not in feature_freq.keys():
                                            feature_freq[wordnet_lemmatizer.lemmatize(target_2)] = 1
                                        else:
                                            feature_freq[wordnet_lemmatizer.lemmatize(target_2)] += 1
                    '''
                    #relation R4.1 other way around
                    elif rel == 'conj':
                        target = pos_sentence[ind][int(dep_indice) - 1][0]
                        if pos_sentence[ind][int(dep_indice) - 1][1] in jj and target not in review_opinion[ind] and target not in punc:
                            review_opinion[ind].append(target)
                            terminate = False
                            if target not in processed_sentiwords:
                                processed_sentiwords.append(target)
                    '''
                    #relation R4.2
                    for line in review:
                        #deal with E~
                        target_2 = line[1]
                        target_2_ind = line[0]
                        if target_2 == '()':
                            origin_2 = line[2][0].lower()
                            for thing in review:
                                if thing != line and (origin_2 == thing[1] or origin_2 == thing[2][0]):
                                    target_2 = thing[1]
                                    target_2_ind = thing[0]
                        if line != item and line[3] == dep_indice and target_2_ind[0] != 'E':
                            rel_j = line[4]
                            #rel == rel_j
    #                        if rel in dep and rel_j in dep:
                            if rel == rel_j or (rel in mods and rel_j in mods) or (rel in sobj[:-1] and rel_j == sobj[-1]) or (rel == sobj[-1] and rel_j in sobj[:-1]):
                                target_2_pos = pos_sentence[ind][int(target_2_ind) - 1][1]
                                if target_2_pos in jj and target_2 not in review_opinion[ind] and target_2 not in punc:
                                    review_opinion[ind].append(target_2)
                                    terminate = False
                                    
                                    target_pair[ind].append([target_2, word])
                                    
                                    if target_2 not in processed_sentiwords:
                                        processed_sentiwords.append(target_2)
                
            
                #relation R4.1               
                if rel == 'conj' and dep_indice[0] != 'E' and indice[0] != 'E':
                    #review[[row[0] for row in review].index(dep_indice)][1]
                    if pos_sentence[ind][int(dep_indice) - 1][0] in processed_sentiwords:
                        target = word
                        if pos_sentence[ind][int(indice) - 1][1] in jj and target not in review_opinion[ind] and target not in punc:
                            review_opinion[ind].append(target)
                            
                            terminate = False
                            target_pair[ind].append([target, pos_sentence[ind][int(dep_indice) - 1][0]])
                            if target not in processed_sentiwords:
                                processed_sentiwords.append(target)
                '''                
                #add relation: target depend on opinion
                if indice[0] != 'E' and pos_sentence[ind][int(indice) - 1][1] in nn:
                    if word not in punc and dep_indice[0] != 'E' and dep_indice != '*':
                        dep_word = pos_sentence[ind][int(dep_indice) - 1][0]
                        if dep_word in processed_sentiwords and rel in dep and word not in review_feature[ind]:
                            review_feature[ind].append(word)
                            if word not in extracted_feature:
                                extracted_feature.append(word)
                            
                            #record the frequency of each lemmatized feature
                            if wordnet_lemmatizer.lemmatize(word) not in feature_freq.keys():
                                feature_freq[wordnet_lemmatizer.lemmatize(word)] = 1
                            else:
                                feature_freq[wordnet_lemmatizer.lemmatize(word)] += 1
                '''         
                    
    #the second iteration to extract feature based on feature and opinion based on feature
    for ind, review in enumerate(processed_reviews):
        if ind not in no_label:

            for item in review:
                dep_indice = item[3]
                rel = item[4]
                word = item[1]
                indice = item[0]
                '''
                #if word in feature set, record it in
                if word in extracted_feature and word not in review_feature[ind]:
                    review_feature[ind].append(word)
                    terminate = False
                elif word in processed_sentiwords and word not in review_opinion[ind]:
                    review_opinion[ind].append(word)
                    terminate = False
                '''    
                #deal with E~
                if word == '()':
                    origin = item[2][0].lower()
                    for thing in review:
                        if thing != item and (origin == thing[1] or origin == thing[2][0]):
                            word = thing[1]
                            indice = thing[0]            
                #extract feature from features
                if word in extracted_feature and dep_indice[0] != 'E':
                    '''
                    #relation R3.1 other way round
                    if rel == 'conj':
                        target = pos_sentence[ind][int(dep_indice) - 1][0]
                        target_pos = pos_sentence[ind][int(dep_indice) - 1][1]
                        if target_pos in nn and target not in review_feature[ind] and target not in punc:
                            review_feature[ind].append(target)
                            terminate = False
                            if target not in extracted_feature:
                                extracted_feature.append(target)  
                            #record the frequency of each lemmatized feature
                            if wordnet_lemmatizer.lemmatize(target) not in feature_freq.keys():
                                feature_freq[wordnet_lemmatizer.lemmatize(target)] = 1
                            else:
                                feature_freq[wordnet_lemmatizer.lemmatize(target)] += 1
                    '''
                    '''
                    #add relation: target depend on opinion
                    if rel in dep:
                        dep_word = pos_sentence[ind][int(dep_indice) - 1][0]
                        if pos_sentence[ind][int(dep_indice) - 1][1] in jj and dep_word not in review_opinion[ind]:
                            review_opinion[ind].append(dep_word)
                            if dep_word not in processed_sentiwords:
                                processed_sentiwords.append(dep_word)
                    '''      
                    
                    #relation R3.2
                    
                    for line in review:
                        #deal with E~
                        target_2 = line[1]
                        target_2_ind = line[0]
                        if target_2 == '()':
                            origin_2 = line[2][0].lower()
                            for thing in review:
                                if thing != line and (origin_2 == thing[1] or origin_2 == thing[2][0]):
                                    target_2 = thing[1]
                                    target_2_ind = thing[0]
                        if line != item and line[3] == dep_indice and target_2_ind[0] != 'E':
                            rel_j = line[4]
                            
                            #rel == rel_j
                            #if rel in dep and rel_j in dep:
                            if rel == rel_j or (rel in mods and rel_j in mods) or (rel in sobj[:-1] and rel_j == sobj[-1]) or (rel == sobj[-1] and rel_j in sobj[:-1]):
                                target_2_pos = pos_sentence[ind][int(target_2_ind) - 1][1]
                                if target_2_pos in nn and target_2 not in review_feature[ind] and target_2 not in punc:
                                    review_feature[ind].append(target_2)
                                    terminate = False
                                    
                                    target_pair[ind].append([target_2, word])
                                    
                                    if target_2 not in extracted_feature:
                                        extracted_feature.append(target_2)
                                    #record the frequency of each lemmatized feature
                                    if wordnet_lemmatizer.lemmatize(target_2) not in feature_freq.keys():
                                        feature_freq[wordnet_lemmatizer.lemmatize(target_2)] = 1
                                    else:
                                        feature_freq[wordnet_lemmatizer.lemmatize(target_2)] += 1
                
            
                #relation R3.1               
                if rel == 'conj' and dep_indice[0] != 'E' and indice[0] != 'E':
                    #review[[row[0] for row in review].index(dep_indice)][1]
                    if pos_sentence[ind][int(dep_indice) - 1][0] in extracted_feature:
                        target = word
                        if pos_sentence[ind][int(indice) - 1][1] in nn and target not in review_feature[ind] and target not in punc:
                            review_feature[ind].append(target)
                            terminate = False
                            
                            target_pair[ind].append([target, pos_sentence[ind][int(dep_indice) - 1][0]])
                            conj_set[ind].append([target, pos_sentence[ind][int(dep_indice) - 1][0]])
                            
                
                            if target not in extracted_feature:
                                extracted_feature.append(target)  
                            #record the frequency of each lemmatized feature
                            if wordnet_lemmatizer.lemmatize(target) not in feature_freq.keys():
                                feature_freq[wordnet_lemmatizer.lemmatize(target)] = 1
                            else:
                                feature_freq[wordnet_lemmatizer.lemmatize(target)] += 1
                            
                #extract opinions from features
                #relation R2.1
                if rel in dep and dep_indice[0] != 'E' and indice[0] != 'E':
                    #review[[row[0] for row in review].index(dep_indice)][1]
                    if pos_sentence[ind][int(dep_indice) - 1][0] in extracted_feature:
                        target = word
                        if pos_sentence[ind][int(indice) - 1][1] in jj and target not in review_opinion[ind] and target not in punc:
                            review_opinion[ind].append(target)
                            terminate = False
                            
                            target_pair[ind].append([target, pos_sentence[ind][int(dep_indice) - 1][0]])
                            
                            if target not in processed_sentiwords:
                                processed_sentiwords.append(target)
                                
                    #relation R2.2 
                    if word in extracted_feature:
                        for line in review:
                            #deal with E~
                            target_2 = line[1]
                            target_2_ind = line[0]
                            if target_2 == '()':
                                origin_2 = line[2][0].lower()
                                for thing in review:
                                    if thing != line and (origin_2 == thing[1] or origin_2 == thing[2][0]):
                                        target_2 = thing[1]
                                        target_2_ind = thing[0]                        
                            if line != item and line[3] == dep_indice and target_2_ind[0] != 'E':
                                rel_2 = line[4]
                        
                                if rel_2 in dep:
                                    target_2_pos = pos_sentence[ind][int(target_2_ind) - 1][1]
                                    if target_2_pos in jj and target_2 not in review_opinion[ind] and target_2 not in punc:
                                        review_opinion[ind].append(target_2)
                                        terminate = False
                                        
                                        target_pair[ind].append([target_2, word])
                                        
                                        if target_2 not in processed_sentiwords:
                                            processed_sentiwords.append(target_2)


feature_dic = cPickle.dump(review_feature, open('feature_dic_implicit', 'w'))  
opinion_dic = cPickle.dump(review_opinion, open('opinion_dic_implicit', 'w')) 

cPickle.dump(feature_freq, open('feature_freq_implicit', 'w'))     
cPickle.dump(conj_set, open('conjunction_set_implicit', 'w'))  
cPickle.dump(target_pair, open('target_pair_implicit', 'w'))      
cPickle.dump(opinion_freq, open('opinion_freq_implicit', 'w'))     

out_feature = open('feat_output_combine_implicit', 'w')
out_opinion = open('opinion_output_combine_implicit', 'w')

for i in range(len(review_feature)):
    out_feature.write(''.join(word + ' ' for word in review_feature[i]))
    out_feature.write('\n')
for j in range(len(review_opinion)):
    out_opinion.write(''.join(word + ' ' for word in review_opinion[j]))
    out_opinion.write('\n')
        
out_feature.close()
out_opinion.close()
