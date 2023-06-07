import ir_datasets
import json
import re
import pathlib

print("Fetching Corpus!....")
main_corpus = {}

dataset = ir_datasets.load('wikir/en1k/training')

count = 0
for doc in dataset.docs_iter():
    if count == 5000:
        break
    main_corpus[doc.doc_id] = doc.text
    count = count + 1

count = 0
expr = ""
for query in dataset.queries_iter():
    if count == 50:
        break
    expr = expr + "^" + query.query_id
    count = count + 1
    if count < 50:
        expr = expr + "|"

for doc in dataset.docs_iter():
    if re.search(expr, doc.doc_id):
        print(doc.doc_id)
        if not main_corpus.get(doc.doc_id):
            main_corpus[doc.doc_id] = doc.text

cwd = pathlib.Path().cwd()

file = cwd.absolute() / 'Files' / 'corpus2.json'

with file.open('w',encoding="utf-8") as corpusfile:
    json.dump(main_corpus, corpusfile)
    corpusfile.close()

print("Done Fetching Corpus!....")