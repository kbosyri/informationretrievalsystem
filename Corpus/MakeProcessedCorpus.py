import requests
import json
import pathlib

cwd = pathlib.Path().cwd()

file = cwd.absolute() / 'Files' / 'corpus.json'

with file.open('r',encoding='utf-8') as corpusfile:
    main_corpus = json.load(corpusfile)
    print("Sending Corpus For Processing")
    processed_corpus = requests.post("http://localhost:5001/api/corpus",json={"input":main_corpus})
    print("Got Response")
    processed_corpus = processed_corpus.json().get('corpus')
    print("Corpus Processed")
    corpusfile.close()

cwd = pathlib.Path().cwd()

file = cwd.absolute() / 'Files' / 'processed_corpus.json'

with file.open('w',encoding='utf-8') as processed_corpus_file:
    json.dump(processed_corpus,processed_corpus_file)
    processed_corpus_file.close()