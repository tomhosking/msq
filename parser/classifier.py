import json
import nltk

from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels

from collections import defaultdict

# import matplotlib.pyplot as plt

import features

MSQ_TYPES = [
    'NONE', # not a question
    'UNK', # question, but not sure of type
    'SEPARABLE',
    'REFORMULATED',
    'ELABORATIVE',
    'DISJUNCTIVE',
    'CONDITIONAL'
]


CLASS_REQUIREMENTS = {
    'SEPARABLE': {
        'pro_q2': True,
        'or': False,
        'if': False,
        'elab_cue': False,
        'qs': False
    },
    'REFORMULATED': {
        'pro_q2': False,
        'vp_ell_q2': False,
        'or': False,
        'if': False,
        'elab_cue': False,
        'qs': False,
        'semantic_overlap': True
    },
    'DISJUNCTIVE': {
        'polar_q1': True,
        'polar_q2': True,
        'or': True,
        'if': False,
        'elab_cue': False,
        'wh_q1': False,
        'wh_q2': False,
        'qs': False
    },
    'CONDITIONAL': {
        'polar_q1': True,
        'if': True,
        'elab_cue': False,
        'wh_q1': False,
        'qs': False
    },
    'ELABORATIVE': {
        'if': False,
        'elab_cue': True
    }
}


class ParsedExample:
    def __init__(self, row):
        self.q1 = row['q1']
        self.q2 = row['q2']
        self.parse1 = nltk.Tree.fromstring(row['parse1'])
        self.parse2 = nltk.Tree.fromstring(row['parse2'])
        



def classify(example):
    feature_dict = features.get_all_feats(example)
    return feats_to_class(feature_dict)    


def feats_to_class(feats):

    for msq_class, mask in CLASS_REQUIREMENTS.items():
        matched = True
        for feat_name, req in mask.items():
            matched = matched and feats[feat_name] == req
        if matched:
            return msq_class
    
    if not feats['pro_q2'] and feats['semantic_overlap']:
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