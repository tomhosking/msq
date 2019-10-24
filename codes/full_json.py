#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 21:00:41 2019

@author: s1574336
"""
import os
import json
from pyexcel_ods3 import get_data
datapath='/afs/inf.ed.ac.uk/group/project/jiechi/gp_nlp/dataset/bonnie/fullset'
json_data={}
attributes=['uri', 'subject', 'content', 'bestanswer', 'selected']
for filename in os.listdir(datapath):
    if filename.endswith('.ods'):
        json_name=os.path.splitext(filename)[0]
        json_data.update({json_name:[]})
        data=get_data(os.path.join(datapath,filename))
        for sheet in data:
            if (data[sheet][0] == attributes):
                idx=1                                    
            else:
                idx=0
            for i in range(idx,len(data[sheet])):
                answer=''
                if len(data[sheet][i])>=3:
                    if len(data[sheet][i])>=4:
                        anwser=data[sheet][i][3]
                    json_data[json_name].append({'uri':data[sheet][i][0],'q1':data[sheet][i][1],'q2':data[sheet][i][2],'answer':answer})
with open('data.json', 'w') as f:

        json.dump(json_data, f)            
