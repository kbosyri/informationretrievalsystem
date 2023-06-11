import math
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import json
from pathlib import Path

cwd = Path().cwd()

file = cwd.absolute() / 'Files' / 'corpus.json'

with file.open('r', encoding='utf-8') as corpusfile:
    main_corpus1 = json.load(corpusfile)
    print("Sending Corpus For Processing")
    corpusfile.close()

file = cwd.absolute() / 'Files' / 'processed_corpus.json'

with file.open('r', encoding='utf-8') as corpusfile:
    processed_corpus1 = json.load(corpusfile)
    print("Got Response")
    corpusfile.close()

file = cwd.absolute() / 'Files' / 'inverted_index.json'

with file.open('r', encoding='utf-8') as corpusfile:
    index1 = json.load(corpusfile)
    corpusfile.close()

file = cwd.absolute() / 'Files' / 'corpus2.json'

with file.open('r', encoding='utf-8') as corpusfile:
    main_corpus2 = json.load(corpusfile)
    print("Sending Corpus For Processing")
    corpusfile.close()

file = cwd.absolute() / 'Files' / 'processed_corpus2.json'

with file.open('r', encoding='utf-8') as corpusfile:
    processed_corpus2 = json.load(corpusfile)
    print("Got Response")
    corpusfile.close()

file = cwd.absolute() / 'Files' / 'inverted_index2.json'

with file.open('r', encoding='utf-8') as corpusfile:
    index2 = json.load(corpusfile)
    corpusfile.close()

def calculate_query_tf(query):
    tf = {}
    terms = requests.post("http://localhost:5001/api/",json={"input":query}).json()['tokens']
    term_count = len(terms)
    for term in terms:
        tf[term] = terms.count(term)/term_count
    return tf

def calculate_query_idf(corpus,query,dataset):
    idf = {}
    n_docs = len(corpus)
    
    if dataset == "1":
        inverted_index = index1
    
    else:
        inverted_index = index2

    terms = requests.post("http://localhost:5001/api/",json={"input":query}).json()['tokens']
    for term in terms:
        if inverted_index.get(term):
            inverted_index[term].append("query")
        else:
            inverted_index[term] = ["query"]
            
    for term, doc_ids in inverted_index.items():
        idf[term] = math.log(n_docs/len(doc_ids))
    return idf

def calculate_query_tfidf(query, corpus,dataset):
    tfidf = {}
    tf = calculate_query_tf(query)
    idf = calculate_query_idf(corpus,query,dataset)
    for term in tf:
        tfidf[term] = tf[term] * idf[term]
    return tfidf


def calculate_tfidf_pandas():
    documents = list(main_corpus.values())
    # Create a TfidfVectorizer object
    vectorizer = TfidfVectorizer()

    # Fit the vectorizer to the documents
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Convert the TF-IDF matrix to a Pandas DataFrame
    df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out(), index=main_corpus.keys())

    # Print the resulting TF-IDF scores
    return df

def calculate_query_tfidf_pandas(query):
    documents = list(corpus.values)
    documents.append(query)

    # Create a TfidfVectorizer object
    vectorizer = TfidfVectorizer()

    # Fit the vectorizer to the documents
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Convert the TF-IDF matrix to a Pandas DataFrame
    df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out(), index=corpus.keys())

    # Print the resulting TF-IDF scores
    return df

file = cwd.absolute() / 'Files' / 'tfidf.json'

with file.open('r', encoding='utf-8') as tfidf_file:
    print("Loading TFIDF Vector!")
    tf_idf = json.load(tfidf_file)
    tfidf_file.close()



def process():
    return tf_idf



def process_pandas():
    
    return calculate_tfidf_pandas()

def process_query(query,dataset):
    if dataset == "1":
        return calculate_query_tfidf(query, main_corpus1,dataset)
    else:
        return calculate_query_tfidf(query, main_corpus2,dataset)

    