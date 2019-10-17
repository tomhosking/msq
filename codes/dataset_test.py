# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 17:46:01 2019

@author: chi
"""

import json


#***************************************************************************

#Sharc- https://sharc-data.github.io/data.html
#sharc_data='/afs/inf.ed.ac.uk/user/s15/s1574336/gp_nlp/dataset/sharc1-official/json/sharc_train.json'
#with open(sharc_data, 'r') as f:
#    sharc_dict = json.load(f)
#sharc_exp=sharc_dict[3]


#***************************************************************************
#QuAC
#quac_data='/afs/inf.ed.ac.uk/user/s15/s1574336/gp_nlp/dataset/quac/val_v0.2.json'
#with open(quac_data, 'r') as f:
#    quac_dict = json.load(f)
#quac_exp=quac_dict['data'][0]['paragraphs']
#quac_exp_ques=quac_exp[0]['qas']


#***************************************************************************
#DuoRC
#duorc_data='C:/Users/chi/Downloads/ParaphraseRC_dev.json'
#with open(duorc_data, 'r') as f:
#    duorc_dict = json.load(f)

#***************************************************************************
#ARC   
#arc_data='/afs/inf.ed.ac.uk/user/s15/s1574336/gp_nlp/dataset/ARC-V1-Feb2018-2/ARC-Easy/ARC-Easy-Dev.jsonl'
#arc_dict=[]
#with open(arc_data, 'r') as f:
#    for line in f:
#        arc_dict.append(json.loads(line))
    

coqa_data='/afs/inf.ed.ac.uk/user/s15/s1574336/gp_nlp/dataset/coqa/coqa-dev-v1.0.json'

with open(coqa_data, 'r') as f:
    coqa_dict = json.load(f)