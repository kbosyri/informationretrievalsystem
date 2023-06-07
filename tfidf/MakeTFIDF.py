import math
import json
import pathlib

cwd = pathlib.Path().cwd()

file = cwd.absolute() / 'Files' / 'corpus.json'

with file.open('r',encoding='utf-8') as corpusfile:
    main_corpus = json.load(corpusfile)
    corpusfile.close()

file = cwd.absolute() / 'Files' / 'processed_corpus.json'

with file.open('r',encoding='utf-8') as processed_corpus_file:
    processed_corpus = json.load(processed_corpus_file)
    processed_corpus_file.close()

file = cwd.absolute() / 'Files' / 'inverted_index.json'

with file.open('r',encoding='utf-8') as indexfile:
    index = json.load(indexfile)
    indexfile.close()

def calculate_tf(document):
    tf = {}
    terms = processed_corpus[document]
    term_count = len(terms)
    for term in terms:
        tf[term] = terms.count(term)/term_count
    return tf

def calculate_idf(corpus):
    idf = {}
    n_docs = len(corpus)
    inverted_index = index
    for term, doc_ids in inverted_index.items():
        idf[term] = math.log(n_docs/len(doc_ids))
    return idf

def calculate_tfidf(document_id, corpus):
    tfidf = {}
    tf = calculate_tf(document_id)
    idf = calculate_idf(corpus)
    for term in tf:
        tfidf[term] = tf[term] * idf[term]
    return tfidf

print("Calculating tfidf vector!..(THIS WILL TAKE A Long TIME!)")
tf_idf = {}
for key in main_corpus.keys():
    tf_idf[key] = calculate_tfidf(key,main_corpus)
print("DONE!...")

file = cwd.absolute() / 'Files' / 'tfidf.json'

with file.open('w',encoding='utf-8') as tfidf_file:
    json.dump(tf_idf, tfidf_file)
    tfidf_file.close()