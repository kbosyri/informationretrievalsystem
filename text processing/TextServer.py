from flask import Flask,request
from textprocessing import Process,ProcessCorpus

app = Flask(__name__)

@app.route("/api/",methods=["POST"])
def server():
    query = request.json.get('input')
    response = {"tokens":Process(query)}

    return response

@app.route('/api/corpus',methods=["POST"])
def ForCorpus():
    print("Processing Corpus")
    corpus = request.json.get('input')
    response = {"corpus":ProcessCorpus(corpus)}
    return response

def query():
    print("Processing Query")
