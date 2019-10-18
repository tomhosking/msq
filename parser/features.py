

import spacy
import numpy as np
import nltk

from collections import defaultdict

nlp = spacy.load("en_core_web_sm")

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

PRONOUNS = [
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

VERB_ELLIPSIS_MARKERS = [
    'do so',
    'did so',
    'does so',
    'do it',
    'do too',
    'does too',
    'did too',
    'did it too',
    'do it too',
    'does it too'
]

WH_WORDS = [
    'who',
    'what',
    'where',
    'when',
    'why',
    'how'
]

POLAR_MARKERS = ["Do",
	"does",
	"did",
	"didn’t",
	"will",
	"won’t",
	"would",
	"is",
	"are",
	"were",
	"weren’t",
	"wasn’t",
	"can",
	"can’t",
	"could",
	"must",
	"have",
	"has",
	"had",
	"hasn’t",
	"haven’t",
	"should",
	"shouldn’t",
	"may",
	"might",
	"shall",
	"ought"]

# What's the threshold semantic cosine similarity to distinguish related qs?
SIMILARITY_THRESHOLD = 0.5

def get_all_feats(example):
    feats = defaultdict(lambda: None)

    feats['pro_q2'] = pro_q2(example)
    feats['vp_ell_q2'] = vp_ell_q2(example)
    feats['polar_q1'] = polar_q1(example)
    feats['polar_q2'] = polar_q2(example)
    feats['wh_q1'] = wh_q1(example)
    feats['wh_q2'] = wh_q2(example)
    feats['elab_cue'] = elab_cue(example)
    feats['or'] = get_or(example)
    feats['if'] = get_if(example)
    feats['qs'] = get_qs(example)
    
    feats['semantic_overlap'] = get_semantic_overlap(example)

    return feats



def pro_q2(example):
    for marker in PRONOUNS:
        if marker in example.q2.lower():
            return True
    return False

def vp_ell_q2(example):
    for marker in VERB_ELLIPSIS_MARKERS:
        if marker in example.q2.lower():
            return True
    return False

def polar_q1(example):
    for marker in POLAR_MARKERS:
        if marker in example.q1.lower():
            return True
    return False

def polar_q2(example):
    for marker in POLAR_MARKERS:
        if marker in example.q1.lower():
            return True
    return False


def wh_q1(example):
    for marker in WH_WORDS:
        if marker in example.q1.lower():
            return True
    return False

def wh_q2(example):
    for marker in WH_WORDS:
        if marker in example.q2.lower():
            return True
    return False

def get_qs(example):
    if '?' not in example.q2.lower():
        return True
    else:
        return False

def elab_cue(example):
    for marker in ELABORATIVE_MARKERS:
        if marker in example.q2.lower():
            return True
    return False

def get_if(example):
    for marker in CONDITIONAL_MARKERS:
        if marker in example.q2.lower():
            return True
    return False
    
def get_or(example):
    if 'or' in example.q2.lower():
        return True
    else:
        return False

def get_semantic_overlap(example):
    q1 = nlp(example.q1)
    q2 = nlp(example.q2)

    similarity = np.dot(q1.vector, q2.vector)/(q1.vector_norm * q2.vector_norm)

    return similarity > SIMILARITY_THRESHOLD