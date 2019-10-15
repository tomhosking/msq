

MSQ_TYPES = [
    'NONE', # not a question
    'UNK', # question, but not sure of type
    'SEPARABLE',
    'REFORMULATED',
    'ELABORATIVE',
    'DISJUNCTIVE',
    'CONDITIONAL'
]

def classify_text(text):
    return 'UNK'


if __name__ == "__main__":
    print(classify_text('Who wrote 1984? Was it published before Brave New World?'))