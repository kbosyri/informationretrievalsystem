import ir_datasets
import re

dataset = ir_datasets.load('antique/train')
qrels1 = {}

for qrel in dataset.qrels_iter():
    if qrel.query_id == "3910705" and re.search("^3910705", qrel.doc_id):
        print(qrel.relevance)
    qrels1[qrel.query_id+","+qrel.doc_id] = qrel.relevance

dataset = ir_datasets.load('wikir/en1k/training')
qrels2 = {}

for qrel in dataset.qrels_iter():
    if qrel.query_id == "3910705" and re.search("^3910705", qrel.doc_id):
        print(qrel.relevance)
    qrels2[qrel.query_id+","+qrel.doc_id] = qrel.relevance

def GetRelevances(result,query,dataset_id):
    response = list()
    qrels = {}

    if dataset_id == "1":
        qrels = qrels1

    else:
        qrels = qrels2
        
    for doc in result:
        doc['relevance'] = qrels.get(query['id'] + "," + doc["id"])
        print("Query ID:"+query['id'])
        print("Doc ID: "+doc['id'])
        print(qrels.get(query['id'] + "," + doc["id"]))
        response.append(doc)

    return response