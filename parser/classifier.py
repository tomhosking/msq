import json, csv
import nltk
from tqdm import tqdm

from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels

from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np

from nltk.tokenize import TreebankWordTokenizer

import features

MSQ_TYPES = [
    'NONE', # not a question
    'UNK', # question, but not sure of type
    'SEPARABLE',
    'REFORMULATION',
    'ELABORATIVE',
    # '2ELAB',
    'DISJUNCTIVE',
    'CONDITIONAL'
]


CLASS_REQUIREMENTS = {
    'SEPARABLE': {
        'pro_q2': True,
        'or': False,
        'if': False,
        'elab_cue': False,
        'qs': False,
        'polar_q1': False,
        'double_pro_q2': False
    },
    'REFORMULATION': {
        'pro_q2': False,
        'vp_ell_q2': False,
        'or': False,
        'if': False,
        'elab_cue': False,
        'qs': False,
        'semantic_overlap': True,
        'sep_cue': False
    },
    'DISJUNCTIVE': {
        'polar_q1': True,
        'polar_q2': True,
        'or': True,
        'if': False,
        'elab_cue': False,
        'wh_q1': False,
        'wh_q2': False,
        'qs': False,
        'sep_cue': False
    },
    'CONDITIONAL': {
        'polar_q1': True,
        'if': True,
        'elab_cue': False,
        'wh_q1': False,
        'sep_cue': False
    },
    'ELABORATIVE': {
        'if': False,
        'elab_cue': True,
        'sep_cue': False
    }
    ,
    'ELABORATIVE2': {
        'if': False,
        'qs': True,
        'semantic_overlap': True,
        'sep_cue': False
    }
}


class ParsedExample:
    def __init__(self, row):
        self.q1 = row['q1']
        self.q2 = row['q2']

        self.q1_toks = q_toks = [tok.lower() for tok in TreebankWordTokenizer().tokenize(self.q1)] # lower after tokenising as case info is useful
        self.q2_toks = q_toks = [tok.lower() for tok in TreebankWordTokenizer().tokenize(self.q2)] # lower after tokenising as case info is useful
        
        # self.parse1 = nltk.Tree.fromstring(row['parse1'])
        # self.parse2 = nltk.Tree.fromstring(row['parse2'])
        



def classify(example):
    feature_dict = features.get_all_feats(example)

    # print(feature_dict)
    # print(example.q1, example.q2)
    # print(feats_to_class(feature_dict))
    # exit()

    pred_class = feats_to_class(feature_dict)

    return 'ELABORATIVE' if pred_class is 'ELABORATIVE2' else pred_class


def feats_to_class(feats):

    for msq_class, mask in CLASS_REQUIREMENTS.items():
        matched = True
        for feat_name, req in mask.items():
            matched = matched and feats[feat_name] == req
        if matched:
            return msq_class
    
    if not feats['pro_q2'] and not feats['semantic_overlap']:
        # No anaphora OR overlap -> unrelated 
        return 'UNK' # could return NONE here - but use UNK for sake of dataset cleanliness
    else:
        # If there _is_ anaphora but no other cues, assume MSQ but unknown type
        return 'UNK'


def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    cls_ixs = unique_labels(y_true, y_pred)
    classes = [classes[ix] for ix in cls_ixs]
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax



if __name__ == "__main__":
    
    # with open('./data/bonnies_msqs_full_dataset.json') as f:
    #     data = json.load(f)

    from os import listdir
    from os.path import isfile, join
    mypath = './data/MSQ_training_data/'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    for filename in onlyfiles:
        print('Parsing {:}'.format(filename))
        with open('./data/MSQ_training_data/'+filename) as f:
            csv_reader = csv.DictReader(f)
        
            data = []
            for ix, row in enumerate(csv_reader):
                if ix > 0:

                    data.append(row)

    # data = [x for k,v in data.items() for x in v]

        class_counts = defaultdict(int)

        class_golds = []
        class_preds = []
        for row in tqdm(data):
            
            pred = classify(ParsedExample(row))
            class_counts[pred] +=1

            # class_preds.append(MSQ_TYPES.index(pred))
            # class_golds.append(MSQ_TYPES.index(row['type_lvb'].upper()))

            row['parser_pred'] = pred

        
        with open('./data/MSQ_training_data_silvered/'+filename.replace('csv','json'), "w") as f:
        # with open('./data/bonnies_msqs_full_silvered', "w") as f:
            json.dump(data, f)

    # print(confusion_matrix(class_golds, class_preds))

    print(class_counts)

    # plot_confusion_matrix(class_golds, class_preds, MSQ_TYPES, normalize=False)
    # plt.show()


    