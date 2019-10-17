#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 19:38:48 2019

@author: s1574336
"""
import json
import nltk

file_path='/afs/inf.ed.ac.uk/user/s15/s1574336/Desktop/bonnies_msqs_pos.json'
with open (file_path) as json_file:
    data=json.load(json_file)
#for i in range(len(data)):
#    sent1=data[i]['q1']
#    sent2=data[i]['q2']
#    token1=nltk.word_tokenize(sent1)
#    token2=nltk.word_tokenize(sent2)
#    pos1=nltk.pos_tag(token1)
#    pos2=nltk.pos_tag(token2)
#    data[i].update({'q1_pos':pos1,'q2_pos':pos2})
#with open ('/afs/inf.ed.ac.uk/user/s15/s1574336/Desktop/bonnies_msqs_nltkpos.json','w') as outfile:
#    json.dump(data,outfile)