from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import json

def filter_data(x):
    if x['parser_pred'] not in ['UNK', 'NONE']:
        return True
    else:
        return False

if __name__ == "__main__":
    with open('./data/MSQ_training_data_silvered/Salesforce_msqs.json') as f:
        data = json.load(f)

    X = [row['q1'] + " " + row['q2'] for row in data if filter_data(row)]
    y = [row['parser_pred'] for row in data if filter_data(row)]

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(X)


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


    clf = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial', class_weight="balanced").fit(X_train, y_train)

    print(clf.score(X_test, y_test))