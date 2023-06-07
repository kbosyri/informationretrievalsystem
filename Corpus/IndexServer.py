from flask import Flask,request
from index import SendIndex,SendCorpus,SendProccessed

app = Flask(__name__)

@app.route("/index",methods=["GET"])
def server():
    print("GOT REQUEST")
    response = {"index":SendIndex()}
    return response

@app.route('/corpus',methods=['GET'])
def CorpusServer():
    print("Sending Corpus")
    response = {'corpus':SendCorpus()}

    return response

@app.route("/processed",methods=["GET"])
def processed():
    print("Sending Corpus")
    response = {'corpus':SendProccessed()}

    return response