import numpy as np
from numpy.linalg import norm
import requests
import json
from pathlib import Path

cwd = Path().cwd()

file = cwd.absolute() / 'Files' / 'tfidf.json'

with file.open('r', encoding='utf-8') as tfidf_file:
    tfidf1 = json.load(tfidf_file)
    tfidf_file.close()

file = cwd.absolute() / 'Files' / 'corpus.json'

with file.open('r', encoding='utf-8') as corpusfile:
    corpus1 = json.load(corpusfile)
    corpusfile.close()

file = cwd.absolute() / 'Files' / 'tfidf2.json'

with file.open('r', encoding='utf-8') as tfidf_file:
    tfidf2 = json.load(tfidf_file)
    tfidf_file.close()

file = cwd.absolute() / 'Files' / 'corpus2.json'

with file.open('r', encoding='utf-8') as corpusfile:
    corpus2 = json.load(corpusfile)
    corpusfile.close()

def CalculateSimilarity(query_vector,docs,dataset):
    ranks = dict()
    tfidf = {}
    query_terms = list(query_vector.keys())
    query_values = list(query_vector.values())
    print(query_terms)
    if dataset == "1":
        tfidf = tfidf1

    else:
        tfidf = tfidf2

    for doc in docs:
        doc_values = []
        for term in query_terms:
            if tfidf[doc].get(term):
                doc_values.append(tfidf[doc].get(term))
            else:
                doc_values.append(0.0)

        ranks[doc] = cosine = np.dot(query_values,doc_values)/(norm(query_values)*norm(doc_values))

    return ranks

def SortResults(ranks,dataset):
    keys = list(ranks.keys())
    values = list(ranks.values())
    sorted_value_index = np.argsort(values)
    sorted_ranks = {keys[i]: values[i] for i in sorted_value_index}
    results = []
    corpus = {}

    if dataset == "1":
        corpus = corpus1

    else:
        corpus = corpus2

    for key,value in sorted_ranks.items():
        results.append({"text":corpus[key],"score":value,"id":key})

    results.reverse()
    return results