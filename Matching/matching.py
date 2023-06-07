import requests
import json
from pathlib import Path

cwd = Path().cwd()

file = cwd.absolute() / 'Files' / 'inverted_index.json'

with file.open('r', encoding='utf-8') as indexfile:
    index1 = json.load(indexfile)
    indexfile.close()

file = cwd.absolute() / 'Files' / 'inverted_index2.json'

with file.open('r', encoding='utf-8') as indexfile:
    index2 = json.load(indexfile)
    indexfile.close()

def isEmpty(dictionary):
    for element in dictionary:
        if element:
            return True
        return False

def match(query_vector,dataset):
    result = set()
    index = {}

    if dataset == "1":
        index = index1

    else:
        index = index2

    for term in query_vector.keys():
        
        if not result:
            print("Empty")
            if index.get(term):
                result = set(index.get(term))
        else:
            print("Not Empty")
            if index.get(term):
                result.update(index.get(term))
    
    return list(result)