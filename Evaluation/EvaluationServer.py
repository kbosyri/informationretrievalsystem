from flask import Flask,request
from evaluate import GetRelevances

app = Flask(__name__)

@app.route('/evaluate',methods=['GET','POST'])
def EvaluationServer():
    results = GetRelevances(request.json.get('result'),request.json.get('query'),request.json.get('dataset'))
    response = {"results":results}
    return response