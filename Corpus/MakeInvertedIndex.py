from collections import defaultdict
import requests
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

def create_inverted_index(corpus):
    inverted_index = defaultdict(list)
    
    for doc_id, doc_content in corpus.items():
        terms = processed_corpus[doc_id]
        for term in terms:
            inverted_index[term].append(doc_id)
    return dict(inverted_index)

file = cwd.absolute() / 'Files' / 'inverted_index.json'

with file.open('w',encoding='utf-8') as indexfile:

    print("Creating Inverted Index!....")
    index = create_inverted_index(main_corpus)
    print("Done Creating Inverted Index")
    json.dump(index, indexfile)
    indexfile.close()