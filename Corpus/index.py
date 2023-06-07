import math
import nltk
import pandas as pd
from collections import defaultdict
import ir_datasets
import requests
import json
import os
from pathlib import Path

cwd = Path().cwd()

file = cwd.absolute() / 'Files' / 'corpus.json'

with file.open('r', encoding='utf-8') as corpusfile:
    print("Fetching Corpus!....")
    main_corpus = json.load(corpusfile)
    print("Done Fetching Corpus!....")
    corpusfile.close()

file = cwd.absolute() / 'Files' / 'processed_corpus.json'

with file.open('r', encoding='utf-8') as corpusfile:
    print("Sending Corpus For Processing")
    processed_corpus = json.load(corpusfile)
    print("Corpus Processed")
    corpusfile.close()

file = cwd.absolute() / 'Files' / 'inverted_index.json'

with file.open('r', encoding='utf-8') as corpusfile:
    print("Creating Inverted Index!....")
    index = json.load(corpusfile)
    print("Done Creating Inverted Index")
    corpusfile.close()


def SendIndex():

    return index

def SendCorpus():
    return main_corpus

def SendProccessed():
    return processed_corpus
