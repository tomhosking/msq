#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 12:12:41 2019

@author: laurie

Script to clean data from Stack Exchange
Input: csv of Stack Exchange data with columns 'title' and 'body'
Output: Two pickle files, one of cleaned data and one of MSQs

"""

import sys
import pandas as pd
import re
import string
from nltk import sent_tokenize
from collections import namedtuple
from progress.bar import Bar


def clean_lines(df_column):
    """Cleans data from Stack Exchange and returns clean lines as list"""
    
    clean_lines = []
    # pattern for html tags
    tag_match = re.compile('<.*?>')
    # patter for website
    website_match = re.compile('https?:\/\/.*[\r\n]*')
    
    for line in df_column:
        s = re.sub(tag_match, '', line)
        s = re.sub(website_match, '[website]', s)
        # replace extra whitespace with spaces
        for x in string.whitespace:
            s = s.replace(x, ' ')
        clean_lines.append(s)
        
    return clean_lines  


def extract_MSQs(line):
    """Extracts pairs of MSQs and the number of chars between q1 and q2"""
    
    tokens = sent_tokenize(line)
    questions = []
    
    for i in range(len(tokens)):
        if tokens[i].endswith('?'):
            q1 = tokens[i]  # find first question
            sep = 0  # counter for separation between end of q1 and start q2
            for j in range(i+1, len(tokens)):  # look for paired question
                if tokens[j].endswith('?'):
                    q2 = tokens[j]
                    questions.append((q1, q2, sep))
                    break
                else:
                    sep += len(tokens[j])

    return questions


def main():
    # check for arguments
    try:
        input_csv = sys.argv[1]
        source = sys.argv[2]
    except IndexError:
        print("Usage is 'python3 clean_stack_exchange.py INPUT_CSV SOURCE'")
        return 1

    
    print("Reading original data")
    # read in and clean csv, overwriting raw data
    original = pd.read_csv(input_csv)
    original['body'] = clean_lines(original['body'])
    
    # extract MSQs into named tuples to keep labelling
    msq = namedtuple('msq', ['title', 'source', 'q1', 'q2', 'sep'])
    msq_list = []
    bar = Bar("Extracting MSQs", max=len(original))
    for row in range(len(original)):
        title = original['title'][row]
        body = original['body'][row]
        questions = extract_MSQs(body)
        source_label = source + '_' + str(row)  # 
        for q1, q2, sep in questions:
            msq_list.append(msq(title, source_label, q1, q2, sep))
        bar.next()
    bar.finish()
    msqs_df = pd.DataFrame(data=msq_list)  # df for output
    
    print("Writing output files")
    # output files as csvs
    original.to_csv("cleaned_data/" + source + "_cleaned.csv", index_label="Index")
    msqs_df.to_csv("cleaned_data/" + source + "_msqs.csv", index=False)
    
    print("Clean csvs of original data and extracted MSQs created")
    
    return 0


if __name__ == "__main__":
    main()
