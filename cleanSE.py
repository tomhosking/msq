#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 12:12:41 2019

@author: laurie

Script to clean data from Stack Exchange
Input: folder containing raw Stack Exchange data 
Output: Two directories, one with cleaned data and one with training MSQs

"""

import sys
import pandas as pd
import re
import string
import glob
from nltk import sent_tokenize
from collections import namedtuple
from progress.bar import Bar
import os


def clean_lines(df_column):
    """Cleans data from Stack Exchange and returns clean lines as list"""
    
    clean_lines = []
    # pattern for html tags
    tag_match = re.compile('<.*?>')
    # patterm for website
    website_match = re.compile('https?:\/\/.*[\r\n]*')
    # pattern for tex
    tex_match = re.compile('\$\$?.+?\$\$?')
    
    for line in df_column:
        s = re.sub(tag_match, '', line)
        s = re.sub(website_match, '[website]', s)
        s = re.sub(tex_match, '[tex]', s)
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


def output_MSQs(df, source):
    """Extracts the MSQs from a cleaned df, outputting a df of training data"""
    
    # extract MSQs into named tuples to keep labelling
    msq = namedtuple('msq', ['title', 'source', 'q1', 'q2', 'sep'])
    msq_list = []
    bar = Bar("Extracting MSQs", max=len(df))
    for row in range(len(df)):
        title = df['title'][row]
        body = df['body'][row]
        questions = extract_MSQs(body)
        source_label = source + '_' + str(row)  # 
        for q1, q2, sep in questions:
            msq_list.append(msq(title, source_label, q1, q2, sep))
        bar.next()
    bar.finish()
    msqs_df = pd.DataFrame(data=msq_list)  # df for output
    return msqs_df


##############################################################################

def main():
    """Cleans directory of Stack Exchange data and returns clean data
    
    Input: directory of raw Stack Exchange data as csvs with columns [title, body]
    Outputs: directory of cleaned data csvs with columns [index, title, body]
        directory of training data csvs with columns ['title', 'source', 'q1', 'q2', 'sep']
    
    """
    
    # read in folder with raw data files from command line
    try:
        folder = sys.argv[1]
    except IndexError:
        print("Usage is `python3 cleanSE.py RAW_DATA_FOLDER")
        return 1
    
    # make clean data directory if none exists
    if not os.path.exists('cleaned_MSQ_files'):
        os.mkdir('cleaned_MSQ_files')
        print('Created `cleaned_MSQ_files` directory')
    else:
        print('`cleaned_MSQ_files` directory already exists')
        
    # make another directory for training data
    if not os.path.exists('MSQ_training_data'):
        os.mkdir('MSQ_training_data')
        print('Created `MSQ_training_data` directory')
    else:
        print('`MSQ_training_data` directory already exists')
    
    
    # read in data for each raw data file
    files = glob.glob(folder + '*_raw.csv')
    for input_csv in files:  # relies on naming convention `FORUM_raw.csv`
        source = input_csv.split('/')[1].split('_')[0]

        print("Reading original data for {}".format(source))
        # read in and clean csv, overwriting raw data
        original = pd.read_csv(input_csv)
        original['body'] = clean_lines(original['body'])
        
        # create DataFrame of MSQ training data
        msqs_df = output_MSQs(original, source)
        
        print("Writing output files")
        # output files as csvs
        original.to_csv("cleaned_MSQ_files/" + source + "_cleaned.csv", 
                        index_label="Index")
        msqs_df.to_csv("MSQ_training_data/" + source + "_msqs.csv", 
                       index=False)
        
        print("Processing of {} completed.".format(source))
        
    return 0


if __name__ == "__main__":
    main()
