import json
import nltk

from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels

from collections import defaultdict

import spacy
import numpy as np
import matplotlib.pyplot as plt

MSQ_TYPES = [
    'NONE', # not a question
    'UNK', # question, but not sure of type
    'SEPARABLE',
    'REFORMULATED',
    'ELABORATIVE',
    'DISJUNCTIVE',
    'CONDITIONAL'
]

ELABORATIVE_MARKERS = [
    'for instance',
    'for example',
    'e.g.',
    'specifically',
    'particularly',
    'in particular',
    'more specifically',
    'more precisely'
]

CONDITIONAL_MARKERS = [
    'if so',
    'accordingly',
    'then',
    'as a result',
    'it follows',
    'subsequently',
    'consequently'
]

COREF_MARKERS = [
    'she',
    'he',
    'it',
    'they',
    'her',
    'his',
    'its',
    'their',
    'them'
]

nlp = spacy.load("en_core_web_sm")


class ParsedExample:
    def __init__(self, row):
        self.q1 = row['q1']
        self.q2 = row['q2']
        self.parse1 = nltk.Tree.fromstring(row['parse1'])
        self.parse2 = nltk.Tree.fromstring(row['parse2'])

def get_coref(example):
    for marker in COREF_MARKERS:
        if marker in example.q2.lower():
            return 1
    return 0

def get_elab_marker(example):
    for marker in ELABORATIVE_MARKERS:
        if marker in example.q2.lower():
            return 1
    return 0

def get_cond_marker(example):
    for marker in CONDITIONAL_MARKERS:
        if marker in example.q2.lower():
            return 1
    return 0
    
def get_disjunctive(example):
    if 'or' in example.q2.lower():
        return True
    else:
        return False

def get_semantic_overlap(example):
    q1 = nlp(example.q1)
    q2 = nlp(example.q2)

    similarity = np.dot(q1.vector, q2.vector)/(q1.vector_norm * q2.vector_norm)

    return similarity


def classify(example):

    feature_dict = {}

    feature_dict['coref'] = get_coref(example)

    feature_dict['elab_marker'] = get_elab_marker(example)
    feature_dict['conditional_marker'] = get_cond_marker(example)
    feature_dict['disjunctive_marker'] = get_disjunctive(example)
    feature_dict['semantic_overlap'] = get_semantic_overlap(example)


    return feats_to_class(feature_dict)    

def feats_to_class(feature_dict):

    if feature_dict['elab_marker'] is +1:
        return 'ELABORATIVE'
    if feature_dict['conditional_marker'] is +1:
        return 'CONDITIONAL'
    
    if feature_dict['coref'] is 0:
        if feature_dict['semantic_overlap'] > 0.8:
            # Reformulated Qs have high overlap without anaphora
            return 'REFORMULATED'
        else:
            # No anaphora OR overlap -> unrelated 
            return 'NONE'
    else:
        # If there _is_ anaphora but no other cues, assume MSQ but unknown type
        return 'UNK'



if __name__ == "__main__":
    
    with open('./data/bonnies_msqs_parsed.json') as f:
        data = json.load(f)

    class_counts = defaultdict(int)

    class_golds = []
    class_preds = []
    for row in data:
        
        pred = classify(ParsedExample(row))
        class_counts[pred] +=1

        class_preds.append(pred)
        class_golds.append(row['type_msq'])

    print(confusion_matrix(class_golds, class_preds))


    print(class_counts)