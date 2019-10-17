import benepar
import json



benepar.download('benepar_en2')

parser = benepar.Parser("benepar_en2")


if __name__ == "__main__":

    
    with open('./data/bonnies_msqs.json') as f:
        data = json.load(f)

    for row in data:

        tree1 = parser.parse(row['q1'])
        tree2 = parser.parse(row['q2'])

        row['parse1'] = str(tree1)
        row['parse2'] = str(tree2)

    
    with open('./data/bonnies_msqs_parsed.json','w') as f:
        json.dump(data, f)

    
    