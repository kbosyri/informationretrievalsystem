from flask import Flask,request
from calculate_tfidf import process,process_pandas,process_query

app = Flask(__name__)

@app.route('/corpus',methods=['GET'])
def corpus_tfidf():
    response = {"tfidf":process()}
    return response

@app.route("/query",methods=["GET","POST"])
def query():
    response = {"query":process_query(request.json.get('input'),request.json.get('dataset'))}
    return response